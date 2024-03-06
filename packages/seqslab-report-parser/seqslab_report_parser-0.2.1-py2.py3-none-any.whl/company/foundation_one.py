import xml.etree.ElementTree as ET

from genomics.maf import MAF
from genomics.vcf import VCF
from parser.const import *
from parser.templates import *
from util.misc_util import *


def get_basic_info(test_name: str, pid: str, pdf_path: str, xml_path: str) -> Dict[str, List[str]]:
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespace = {'rr': 'http://integration.foundationmedicine.com/reporting'}
        r = root.find('rr:CustomerInformation/rr:TRF', namespace).text
        first_name = root.find('rr:ResultsPayload/FinalReport/PMI/FirstName', namespace).text
        last_name = root.find('rr:ResultsPayload/FinalReport/PMI/LastName', namespace).text
        date = root.find('rr:ResultsPayload/FinalReport/PMI/CollDate', namespace).text
        tumor = root.find('rr:ResultsPayload/FinalReport/PMI/SubmittedDiagnosis', namespace).text
        specimen_site = root.find('rr:ResultsPayload/FinalReport/PMI/SpecSite', namespace).text

        return {
            REPORT_TEST_ASSAY: [test_name],
            REPORT_PATIENT_ID: [pid],
            REPORT_PATIENT_NAME: [f'{first_name} {last_name}'],
            REPORT_ID: [r],
            REPORT_DATE: [date],
            REPORT_DIAGNOSIS: [tumor],
            REPORT_SAMPLED_TISSUE: [specimen_site]
        }
    except ET.ParseError as e:
        print(f'Error parsing XML file: {e}')


def get_test_type(file_path: str) -> str:
    tree = ET.parse(file_path)
    root = tree.getroot()

    namespace = {'rr': 'http://integration.foundationmedicine.com/reporting'}
    test_type = root.find('rr:ResultsPayload/FinalReport/Sample/TestType', namespace).text
    return test_type


def get_gene_findings_and_biomarkers(xml_path: str) -> (List[Dict[str, List[str]]], List[Dict[str, List[str]]]):
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespace = {'rr': 'http://integration.foundationmedicine.com/reporting'}
        genes = root.findall('rr:ResultsPayload/FinalReport/Genes/Gene', namespace)
        biomarkers = []
        findings = []
        for gene in genes:
            b = {BIOMARKER: [], RESULTS: []}
            d = {BIOMARKER: [], BIOMARKER_ACTIONABLE_DRUG: [], BIOMARKER_CANDIDATE_DRUG: []}
            for child in gene:
                if child.tag == 'Name':
                    if len(child.text.split(' ')) > 1:
                        b[BIOMARKER] = [child.text]
                    else:
                        d[BIOMARKER].append(child.text)
                if child.tag == 'Alterations':
                    for alteration in child:
                        for a in alteration:
                            if a.tag == 'Name':
                                if b[BIOMARKER]:
                                    b[RESULTS] = [a.text]
                                else:
                                    d[BIOMARKER].append(a.text)
                            if a.tag == 'Therapies':
                                for therapy in a:
                                    fda_approved = False
                                    drug = ''
                                    for t in therapy:
                                        if t.tag == 'GenericName':
                                            drug = t.text
                                        if t.tag == 'FDAApproved' and t.text == 'true':
                                            fda_approved = True
                                    if fda_approved:
                                        d[BIOMARKER_ACTIONABLE_DRUG].append(drug)
                                    else:
                                        d[BIOMARKER_CANDIDATE_DRUG].append(drug)
            d[BIOMARKER_ACTIONABLE_DRUG] = list(set(d[BIOMARKER_ACTIONABLE_DRUG]))
            d[BIOMARKER_CANDIDATE_DRUG] = list(set(d[BIOMARKER_CANDIDATE_DRUG]))
            if d[BIOMARKER]:
                findings.append(d)
            if b[BIOMARKER]:
                biomarkers.append(b)

        return findings, biomarkers
    except ET.ParseError as e:
        print(f'Error parsing XML file: {e}')


def get_variant(xml_path: str) -> List[Dict[str, List[str]]]:
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespace = {'rr': 'http://integration.foundationmedicine.com/reporting',
                     'vv': 'http://foundationmedicine.com/compbio/variant-report-external'}
        short_variants = root.findall('rr:ResultsPayload/vv:variant-report/vv:short-variants/vv:short-variant', namespace)
        variants = []
        for variant in short_variants:
            v = {
                GENE: [variant.attrib['gene']],
                VARIANT_POSITION: [variant.attrib['position']],
                VARIANT_HGVS: [variant.attrib['cds-effect']],
                VARIANT_AMINO_ACID_CHANGE: [variant.attrib['protein-effect']],
                VARIANT_COVERAGE: [variant.attrib['depth']],
                VARIANT_ALLELE_FRACTION: [variant.attrib['allele-fraction']],
                VARIANT_ACCESSION: [variant.attrib['transcript']],
                VARIANT_EFFECT: [variant.attrib['functional-effect']],
                VARIANT_STRAND: [variant.attrib['strand']]
            }

            variants.append(v)

        return variants
    except ET.ParseError as e:
        print(f'Error parsing XML file: {e}')


def get_cna(xml_path: str) -> List[Dict[str, List[str]]]:
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespace = {'rr': 'http://integration.foundationmedicine.com/reporting',
                     'vv': 'http://foundationmedicine.com/compbio/variant-report-external'}
        alterations = root.findall('rr:ResultsPayload/vv:variant-report/vv:copy-number-alterations/vv:copy-number-alteration', namespace)
        cnvs = []
        for a in alterations:
            v = {
                GENE: [a.attrib['gene']],
                CHROMOSOME: [a.attrib['position']],
                COPY_NUMBER: [a.attrib['copy-number']],
                VARIANT_FORM: [a.attrib['type']]
            }

            cnvs.append(v)

        return cnvs
    except ET.ParseError as e:
        print(f'Error parsing XML file: {e}')


def get_fusion(xml_path: str) -> List[Dict[str, List[str]]]:
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()

        namespace = {'rr': 'http://integration.foundationmedicine.com/reporting',
                     'vv': 'http://foundationmedicine.com/compbio/variant-report-external'}
        rearrangements = root.findall('rr:ResultsPayload/vv:variant-report/vv:rearrangements/vv:rearrangement', namespace)
        fusions = []
        for a in rearrangements:
            description = a.attrib['description']
            if a.attrib['type'] == 'fusion':
                gene_a = a.attrib['targeted-gene']
                gene_b = a.attrib['other-gene']
                pattern = r'\w+\((\w+)\)-\w+\((\w+)\) fusion \(\w(\d+\*?); \w(\d+\*?)\)'
                (acc_num_a, acc_num_b, exon_a, exon_b) = re.findall(pattern, description)[0]
                v = {
                    FUSION_VARIANT: [f'{gene_a}-{gene_b} fusion'],
                    FUSION_GENE: [f"{gene_a} and {gene_b}"],
                    FUSION_BREAKPOINT: [f"exon {exon_a} of the {gene_a} gene and exon {exon_b} of the {gene_b} gene"],
                    FUSION_TRANSCRIPT:  [f"{acc_num_a} and {acc_num_b}"]
                }

                fusions.append(v)

        return fusions
    except ET.ParseError as e:
        print(f'Error parsing XML file: {e}')
    except Exception:
        print(f'Error parsing regular expression')


def parse_foundation_one(
        test_name: str,
        patient_id: str,
        maf: MAF,
        vcf: VCF,
        pdf_file_path: str,
        xml_file_path: str) -> (Dict, str, List[Dict[str, str]]):
    results = {
        'test_name': test_name,
        'label': patient_id,
    }
    basic_info = get_basic_info(test_name, patient_id, pdf_file_path, xml_file_path)
    results['report'] = substitute_variables(template_report, basic_info)

    (findings, biomarkers) = get_gene_findings_and_biomarkers(xml_file_path)
    r = []
    for a in findings:
        if a[BIOMARKER_ACTIONABLE_DRUG]:
            a[BIOMARKER_MUTATION] = a[BIOMARKER]
            a[BIOMARKER_EFFECT] = ['FDA-approved']
            r.append(substitute_variables(template_biomarker_sens, a))
        if a[BIOMARKER_CANDIDATE_DRUG]:
            a[BIOMARKER_MUTATION] = a[BIOMARKER]
            a[BIOMARKER_EFFECT] = ['FDA-approved']
            r.append(substitute_variables(template_biomarker_other, a))
    results['biomarker'] = r if r else None
    biomarker_to_therapy = convert_therapy_info_to_map(findings, get_substring_until_parenthesis)

    r = [{
        "text": 'Immune checkpoint inhibitor biomarkers:',
        "tokens": ['Immune', 'checkpoint', 'inhibitor', 'biomarkers:'],
        "tags": ['O', 'O', 'O', 'O'],
        "tags_ids": [label_dict['O'], label_dict['O'], label_dict['O'], label_dict['O']],
        "ner": {}
    }]
    for b in biomarkers:
        if "Tumor Mutational Burden" in ' '.join(b[BIOMARKER]):
            b[TMB_RESULT] = b[RESULTS] + ["Muts/Mb"]
            r.append(substitute_variables(template_ici_tmb, b))
        elif "Microsatellite" in ''.join(b[BIOMARKER]):
            b[MSI_RESULT] = b[RESULTS]
            r.append(substitute_variables(template_ici_msi, b))
    results['ici_biomarker'] = r if len(r) > 1 else None
    results['ici_biomarker-therapy'] = with_therapy(
        r[1:],
        biomarker_to_therapy,
        lambda i: [extract_substring_in_parentheses(i['ner'].get(TMB_RESULT, '')), extract_substring_in_parentheses(i['ner'].get(MSI_RESULT, ''))])

    # TODO
    template_foundation_variant = \
        "A DNA sequence variant {VARIANT_HGVS} is detected in the chromosome {VARIANT_POSITION} of the {GENE} gene " \
        "located on the {VARIANT_STRAND} strand, resulting in an amino acid change {VARIANT_AMINO_ACID_CHANGE}. The " \
        "variant allele frequency indicates that approximately {VARIANT_ALLELE_FRACTION} of the sequenced reads carry" \
        " this specific mutation with coverage of {VARIANT_COVERAGE}. This mutation causes {VARIANT_EFFECT} variant " \
        "effect. The transcripts associated with the variant are identified by the accession numbers " \
        "{VARIANT_ACCESSION}."
    r = []
    variants = get_variant(xml_file_path)
    for a in variants:
        if maf:
            maf_info = maf.to_maf(basic_info[REPORT_PATIENT_ID][0], a)
            maf_dict = {k: [v] for k, v in maf_info.items()}
            a.update(maf_dict)
        r.append(substitute_variables(template_foundation_variant, a))
    results['variant'] = r if len(r) > 1 else None
    results['variant-therapy'] = with_therapy(r, biomarker_to_therapy, lambda i: [i['ner'][GENE], i['ner'][VARIANT_AMINO_ACID_CHANGE]])

    r = []
    cnas = get_cna(xml_file_path)
    for a in cnas:
        r.append(substitute_variables(template_cna, a))
    results['cna'] = r if len(r) > 1 else None
    results['cna-therapy'] = with_therapy(r, biomarker_to_therapy, lambda i: [i['ner'][GENE], i['ner'][VARIANT_FORM]])

    r = []
    fusions = get_fusion(xml_file_path)
    for f in fusions:
        r.append(substitute_variables(template_fusion_no_variant_form, f))
    results['fusion'] = r if r else None
    results['fusion-therapy'] = with_therapy(r, biomarker_to_therapy, lambda i: i['ner'][FUSION_VARIANT].split(' ')[0])

    if vcf:
        vcf_header, vcf = vcf.to_vcf('FOUNDATION', basic_info[REPORT_PATIENT_ID][0], variants)
        return results, vcf_header, vcf
    else:
        return results, None, []
