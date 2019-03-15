# Copyright 2019 by Jens Thomas.  All rights reserved.
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.

"""Tests for SearchIO HhsuiteIO parsers."""


import os
import unittest

from Bio.SearchIO import parse


# test case files are in the Blast directory
TEST_DIR = 'HHsuite'
FMT = 'hhsuite2-text'


def get_file(filename):
    """Returns the path of a test file."""
    return os.path.join(TEST_DIR, filename)


class HhsuiteCases(unittest.TestCase):

    def test_2uvo(self):
        "Test parsing 2uvo"

        txt_file = get_file('2uvo_hhblits.hhr')
        qresults = parse(txt_file, FMT)

        # test first and only qresult
        qresult = next(qresults)

        nhits = 32
        self.assertEqual('HHSUITE', qresult.program)
        self.assertEqual('2UVO:A|PDBID|CHAIN|SEQUENCE', qresult.id)
        self.assertEqual(171, qresult.seq_len)
        self.assertEqual(nhits, len(qresult))

        hit = qresult[0]
        self.assertEqual('2uvo_A_1', hit.id)
        self.assertEqual('Agglutinin isolectin 1; carbohydrate-binding protein, hevein domain, chitin-binding,'
                         ' GERM agglutinin, chitin-binding protein; HET: NDG NAG GOL; 1.40A {Triticum aestivum}'
                         ' PDB: 1wgc_A* 2cwg_A* 2x3t_A* 4aml_A* 7wga_A 9wga_A 2wgc_A 1wgt_A 1k7t_A* 1k7v_A* 1k7u_A'
                         ' 2x52_A* 1t0w_A*', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(3.7e-34, hit.evalue)
        self.assertEqual(210.31, hit.score)
#         self.assertEqual(0.5, hit.bias)
#         self.assertEqual(1.5, hit.domain_exp_num)
#         self.assertEqual(1, hit.domain_obs_num)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
#         self.assertEqual(1, hsp.domain_index)
        self.assertTrue(hsp.is_included)
        self.assertEqual(210.31, hsp.score)
#         self.assertEqual(0.5, hsp.bias)
#         self.assertEqual(5e-40, hsp.evalue_cond)
        self.assertEqual(3.7e-34, hsp.evalue)
        self.assertEqual(1, hsp.hit_start)
        self.assertEqual(171, hsp.hit_end)
#         self.assertEqual('.]', hsp.hit_endtype)
        self.assertEqual(1, hsp.query_start)
        self.assertEqual(171, hsp.query_end)
#         self.assertEqual('..', hsp.query_endtype)
#         self.assertEqual(130, hsp.env_start)
#         self.assertEqual(205, hsp.env_end)
#         self.assertEqual('..', hsp.env_endtype)
#         self.assertEqual(0.97, hsp.acc_avg)
        self.assertEqual('ERCGEQGSNMECPNNLCCSQYGYCGMGGDYCGKGCQNGACWTSKRCGSQAGGATCTNNQCCSQYGYCGFGAEYC'
                         'GAGCQGGPCRADIKCGSQAGGKLCPNNLCCSQWGFCGLGSEFCGGGCQSGACSTDKPCGKDAGGRVCTNNYCCS'
                         'KWGSCGIGPGYCGAGCQSGGCDG',
                         str(hsp.hit.seq))
        self.assertEqual('ERCGEQGSNMECPNNLCCSQYGYCGMGGDYCGKGCQNGACWTSKRCGSQAGGATCTNNQCCSQYGYCGFGAEYC'
                         'GAGCQGGPCRADIKCGSQAGGKLCPNNLCCSQWGFCGLGSEFCGGGCQSGACSTDKPCGKDAGGRVCTNNYCCS'
                         'KWGSCGIGPGYCGAGCQSGGCDG',
                         str(hsp.query.seq))
#         self.assertEqual('67899******************************************************************96',
#                          hsp.aln_annotation['PP'])

        # Check last hit
        hit = qresult[nhits - 1]
        self.assertEqual('1wga_2', hit.id)
        self.assertEqual('lectin (agglutinin); NMR {}', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(2.6, hit.evalue)
        self.assertEqual(25.90, hit.score)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
        self.assertTrue(hsp.is_included)
        self.assertEqual(2.6, hsp.evalue)
        self.assertEqual(25.90, hsp.score)
        self.assertEqual(11, hsp.hit_start)
        self.assertEqual(116, hsp.hit_end)
        self.assertEqual(54, hsp.query_start)
        self.assertEqual(163, hsp.query_end)
        self.assertEqual('XCXXXXCCXXXXXCXXXXXXCXXXCXXXXCXXXXXCXXX--XXXCXXXXCCXXXXXCXXXXXXCXXXCXXXXCXXXXXCX'
                         'XX--XXXCXXXXCCXXXXXCXXXXXXCXXX',
                         str(hsp.hit.seq))
        self.assertEqual('TCTNNQCCSQYGYCGFGAEYCGAGCQGGPCRADIKCGSQAGGKLCPNNLCCSQWGFCGLGSEFCGGGCQSGACSTDKPCG'
                         'KDAGGRVCTNNYCCSKWGSCGIGPGYCGAG',
                         str(hsp.query.seq))

    def test_2uvo_onlyheader(self):
        "Test parsing 4uvo with only header present"

        txt_file = get_file('2uvo_hhblits_onlyheader.hhr')
        qresults = parse(txt_file, FMT)

        with self.assertRaises(RuntimeError):
            next(qresults)

    def test_2uvo_emptytable(self):
        "Test parsing 4uvo with empty results table"

        txt_file = get_file('2uvo_hhblits_emptytable.hhr')
        qresults = parse(txt_file, FMT)

        with self.assertRaises(RuntimeError):
            next(qresults)

    def test_allx(self):
        "Test parsing allx.hhr"

        txt_file = get_file('allx.hhr')
        qresults = parse(txt_file, FMT)

        # test first and only qresult
        qresult = next(qresults)

        nhits = 10
        self.assertEqual('HHSUITE', qresult.program)
        self.assertEqual('Only X amino acids', qresult.id)
        self.assertEqual(39, qresult.seq_len)
        self.assertEqual(nhits, len(qresult))

        hit = qresult[0]
        self.assertEqual('1klr_A_1', hit.id)
        self.assertEqual('Zinc finger Y-chromosomal protein; transcription; NMR {Synthetic} SCOP: g.37.1.1 PDB: '
                         '5znf_A 1kls_A 1xrz_A* 7znf_A', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(3.4E+04, hit.evalue)
        self.assertEqual(-0.01, hit.score)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
        self.assertTrue(hsp.is_included)
        self.assertEqual(3.4E+04, hsp.evalue)
        self.assertEqual(-0.01, hsp.score)
        self.assertEqual(24, hsp.hit_start)
        self.assertEqual(24, hsp.hit_end)
        self.assertEqual(39, hsp.query_start)
        self.assertEqual(39, hsp.query_end)
        self.assertEqual('T', str(hsp.hit.seq))
        self.assertEqual('X', str(hsp.query.seq))

        # Check last hit
        hit = qresult[nhits - 1]
        self.assertEqual('1zfd_A_1', hit.id)
        self.assertEqual('SWI5; DNA binding motif, zinc finger DNA binding domain; NMR {Saccharomyces cerevisiae}'
                         ' SCOP: g.37.1.1', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(3.6e+04, hit.evalue)
        self.assertEqual(0.03, hit.score)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
        self.assertTrue(hsp.is_included)
        self.assertEqual(3.6e+04, hsp.evalue)
        self.assertEqual(0.03, hsp.score)
        self.assertEqual(1, hsp.hit_start)
        self.assertEqual(1, hsp.hit_end)
        self.assertEqual(4, hsp.query_start)
        self.assertEqual(4, hsp.query_end)
        self.assertEqual('D', str(hsp.hit.seq))
        self.assertEqual('X', str(hsp.query.seq))

    def test_4y9h_nossm(self):
        "Test parsing 4y9h_hhsearch_server_NOssm.hhr"

        txt_file = get_file('4y9h_hhsearch_server_NOssm.hhr')
        qresults = parse(txt_file, FMT)

        # test first and only qresult
        qresult = next(qresults)

        nhits = 29
        self.assertEqual('HHSUITE', qresult.program)
        self.assertEqual('4Y9H:A|PDBID|CHAIN|SEQUENCE', qresult.id)
        self.assertEqual(226, qresult.seq_len)
        self.assertEqual(nhits, len(qresult))

        hit = qresult[0]
        self.assertEqual('5ZIM_A_1', hit.id)
        self.assertEqual('Bacteriorhodopsin; proton pump, membrane protein, PROTON; HET: L2P, RET; 1.25A {Halobacterium'
                         ' salinarum}; Related PDB entries: 1R84_A 1KG8_A 1KME_B 1KGB_A 1KG9_A 1KME_A 4X31_A 5ZIL_A 1E0P_A '
                         '4X32_A 5ZIN_A 1S53_B 1S51_B 1S53_A 1S54_A 1F50_A 1S54_B 1S51_A 1F4Z_A 5J7A_A 1S52_B 1S52_A 4Y9H_A '
                         '3T45_A 3T45_C 3T45_B 1C3W_A 1L0M_A', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(2.1e-48, hit.evalue)
        self.assertEqual(320.44, hit.score)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
        self.assertTrue(hsp.is_included)
        self.assertEqual(2.1e-48, hsp.evalue)
        self.assertEqual(320.44, hsp.score)
        self.assertEqual(2, hsp.hit_start)
        self.assertEqual(227, hsp.hit_end)
        self.assertEqual(1, hsp.query_start)
        self.assertEqual(226, hsp.query_end)
        self.assertEqual('GRPEWIWLALGTALMGLGTLYFLVKGMGVSDPDAKKFYAITTLVPAIAFTMYLSMLLGYGLTMVPFGGEQNPIYWARYAD'
                         'WLFTTPLLLLDLALLVDADQGTILALVGADGIMIGTGLVGALTKVYSYRFVWWAISTAAMLYILYVLFFGFTSKAESMRP'
                         'EVASTFKVLRNVTVVLWSAYPVVWLIGSEGAGIVPLNIETLLFMVLDVSAKVGFGLILLRSRAIFG', str(hsp.hit.seq))
        self.assertEqual('GRPEWIWLALGTALMGLGTLYFLVKGMGVSDPDAKKFYAITTLVPAIAFTMYLSMLLGYGLTMVPFGGEQNPIYWARYAD'
                         'WLFTTPLLLLDLALLVDADQGTILALVGADGIMIGTGLVGALTKVYSYRFVWWAISTAAMLYILYVLFFGFTSKAESMRP'
                         'EVASTFKVLRNVTVVLWSAYPVVWLIGSEGAGIVPLNIETLLFMVLDVSAKVGFGLILLRSRAIFG', str(hsp.query.seq))

        # Check last hit
        hit = qresult[nhits - 1]
        self.assertEqual('5ABB_Z_1', hit.id)
        self.assertEqual('PROTEIN TRANSLOCASE SUBUNIT SECY, PROTEIN; TRANSLATION, RIBOSOME, MEMBRANE PROTEIN, '
                         'TRANSLOCON; 8.0A {ESCHERICHIA COLI}', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(3.3e-05, hit.evalue)
        self.assertEqual(51.24, hit.score)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
        self.assertTrue(hsp.is_included)
        self.assertEqual(3.3e-05, hsp.evalue)
        self.assertEqual(51.24, hsp.score)
        self.assertEqual(15, hsp.hit_start)
        self.assertEqual(65, hsp.hit_end)
        self.assertEqual(8, hsp.query_start)
        self.assertEqual(59, hsp.query_end)
        self.assertEqual('FWLVTAALLASTVFFFVERDRVS-AKWKTSLTVSGLVTGIAFWHYMYMRGVW', str(hsp.hit.seq))
        self.assertEqual('LALGTALMGLGTLYFLVKGMGVSDPDAKKFYAITTLVPAIAFTMYLSMLLGY', str(hsp.query.seq))

    def test_q9bsu1(self):
        "Test parsing hhsearch_q9bsu1_uniclust_w_ss_pfamA_30.hhr"

        txt_file = get_file('hhsearch_q9bsu1_uniclust_w_ss_pfamA_30.hhr')
        qresults = parse(txt_file, FMT)

        # test first and only qresult
        qresult = next(qresults)

        nhits = 16
        self.assertEqual('HHSUITE', qresult.program)
        self.assertEqual('sp|Q9BSU1|CP070_HUMAN UPF0183 protein C16orf70 OS=Homo sapiens OX=9606 GN=C16orf70'
                         ' PE=1 SV=1', qresult.id)
        self.assertEqual(422, qresult.seq_len)
        self.assertEqual(nhits, len(qresult))

        hit = qresult[0]
        self.assertEqual('PF03676.13_1', hit.id)
        self.assertEqual('UPF0183 ; Uncharacterised protein family (UPF0183)', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(2e-106, hit.evalue)
        self.assertEqual(822.75, hit.score)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
        self.assertTrue(hsp.is_included)
        self.assertEqual(2e-106, hsp.evalue)
        self.assertEqual(822.75, hsp.score)
        self.assertEqual(1, hsp.hit_start)
        self.assertEqual(395, hsp.hit_end)
        self.assertEqual(11, hsp.query_start)
        self.assertEqual(407, hsp.query_end)
        self.assertEqual('SLGNEQWEFTLGMPLAQAVAILQKHCRIIKNVQVLYSEQSPLSHDLILNLTQDGIKLMFDAFNQRLKVIEVCDLTKVKLK'
                         'YCGVHFNSQAIAPTIEQIDQSFGATHPGVYNSAEQLFHLNFRGLSFSFQLDSWTEAPKYEPNFAHGLASLQIPHGATVKR'
                         'MYIYSGNSLQDTKAPMMPLSCFLGNVYAESVDVLRDGTGPAGLRLRLLAAGCGPGLLADAKMRVFERSVYFGDSCQDVLS'
                         'MLGSPHKVFYKSEDKMKIHSPSPHKQVPSKCNDYFFNYFTLGVDILFDANTHKVKKFVLHTNYPGHYNFNIYHRCEFKIP'
                         'LAIKKENADGQTE--TCTTYSKWDNIQELLGHPVEKPVVLHRSSSPNNTNPFGSTFCFGLQRMIFEVMQNNHIASVTLY',
                         str(hsp.query.seq))
        self.assertEqual('EQWE----FALGMPLAQAISILQKHCRIIKNVQVLYSEQMPLSHDLILNLTQDGIKLLFDACNQRLKVIEVYDLTKVKLK'
                         'YCGVHFNSQAIAPTIEQIDQSFGATHPGVYNAAEQLFHLNFRGLSFSFQLDSWSEAPKYEPNFAHGLASLQIPHGATVKR'
                         'MYIYSGNNLQETKAPAMPLACFLGNVYAECVEVLRDGAGPLGLKLRLLTAGCGPGVLADTKVRAVERSIYFGDSCQDVLS'
                         'ALGSPHKVFYKSEDKMKIHSPSPHKQVPSKCNDYFFNYYILGVDILFDSTTHLVKKFVLHTNFPGHYNFNIYHRCDFKIP'
                         'LIIKKDGADAHSEDCILTTYSKWDQIQELLGHPMEKPVVLHRSSSANNTNPFGSTFCFGLQRMIFEVMQNNHIASVTLY',
                         str(hsp.hit.seq))

        # Check last hit
        hit = qresult[nhits - 1]
        self.assertEqual('PF10049.8_1', hit.id)
        self.assertEqual('DUF2283 ; Protein of unknown function (DUF2283)', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(78, hit.evalue)
        self.assertEqual(19.81, hit.score)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
        self.assertTrue(hsp.is_included)
        self.assertEqual(78, hsp.evalue)
        self.assertEqual(19.81, hsp.score)
        self.assertEqual(26, hsp.hit_start)
        self.assertEqual(48, hsp.hit_end)
        self.assertEqual(62, hsp.query_start)
        self.assertEqual(85, hsp.query_end)
        self.assertEqual('APNVIFDYDA-EGRIVGIELLDAR', str(hsp.hit.seq))
        self.assertEqual('QDGIKLMFDAFNQRLKVIEVCDLT', str(hsp.query.seq))

    def test_4p79(self):
        "Test parsing 4p79_hhsearch_server_NOssm.hhr"

        txt_file = get_file('4p79_hhsearch_server_NOssm.hhr')
        qresults = parse(txt_file, FMT)

        # test first and only qresult
        qresult = next(qresults)

        nhits = 8
        self.assertEqual('HHSUITE', qresult.program)
        self.assertEqual('4P79:A|PDBID|CHAIN|SEQUENCE', qresult.id)
        self.assertEqual(198, qresult.seq_len)
        self.assertEqual(nhits, len(qresult))

        hit = qresult[0]
        self.assertEqual('4P79_A_1', hit.id)
        self.assertEqual('cell adhesion protein; cell adhesion, tight junction, membrane; HET: OLC'
                         ', MSE; 2.4A {Mus musculus}', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(6.8e-32, hit.evalue)
        self.assertEqual(194.63, hit.score)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
        self.assertTrue(hsp.is_included)
        self.assertEqual(6.8e-32, hsp.evalue)
        self.assertEqual(194.63, hsp.score)
        self.assertEqual(1, hsp.hit_start)
        self.assertEqual(198, hsp.hit_end)
        self.assertEqual(1, hsp.query_start)
        self.assertEqual(198, hsp.query_end)
        self.assertEqual('GSEFMSVAVETFGFFMSALGLLMLGLTLSNSYWRVSTVHGNVITTNTIFENLWYSCATDSLGVSNCWDFPSMLALSGYVQ'
                         'GCRALMITAILLGFLGLFLGMVGLRATNVGNMDLSKKAKLLAIAGTLHILAGACGMVAISWYAVNITTDFFNPLYAGTKY'
                         'ELGPALYLGWSASLLSILGGICVFSTAAASSKEEPATR', str(hsp.query.seq))
        self.assertEqual('GSEFMSVAVETFGFFMSALGLLMLGLTLSNSYWRVSTVHGNVITTNTIFENLWYSCATDSLGVSNCWDFPSMLALSGYVQ'
                         'GCRALMITAILLGFLGLFLGMVGLRATNVGNMDLSKKAKLLAIAGTLHILAGACGMVAISWYAVNITTDFFNPLYAGTKY'
                         'ELGPALYLGWSASLLSILGGICVFSTAAASSKEEPATR', str(hsp.hit.seq))

        # Check last hit
        hit = qresult[nhits - 1]
        self.assertEqual('5YQ7_F_1', hit.id)
        self.assertEqual('Beta subunit of light-harvesting 1; Photosynthetic core complex, PHOTOSYNTHESIS; '
                         'HET: MQE, BCL, HEM, KGD, BPH;{Roseiflexus castenholzii}; Related PDB entries: 5YQ7_V'
                         ' 5YQ7_3 5YQ7_T 5YQ7_J 5YQ7_9 5YQ7_N 5YQ7_A 5YQ7_P 5YQ7_H 5YQ7_D 5YQ7_5 5YQ7_7 5YQ7_1 '
                         '5YQ7_R', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(6.7, hit.evalue)
        self.assertEqual(20.51, hit.score)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
        self.assertTrue(hsp.is_included)
        self.assertEqual(6.7, hsp.evalue)
        self.assertEqual(20.51, hsp.score)
        self.assertEqual(9, hsp.hit_start)
        self.assertEqual(42, hsp.hit_end)
        self.assertEqual(6, hsp.query_start)
        self.assertEqual(37, hsp.query_end)
        self.assertEqual('RTSVVVSTLLGLVMALLIHFVVLSSGAFNWLRAP', str(hsp.hit.seq))
        self.assertEqual('SVAVETFGFFMSALGLLMLGLTLSNS--YWRVST', str(hsp.query.seq))

    def test_9590198(self):
        "Test parsing hhpred_9590198.hhr"

        txt_file = get_file('hhpred_9590198.hhr')
        qresults = parse(txt_file, FMT)

        # test first and only qresult
        qresult = next(qresults)

        nhits = 34
        self.assertEqual('HHSUITE', qresult.program)
        self.assertEqual('sp|Q9BSU1|CP070_HUMAN UPF0183 protein C16orf70 OS=Homo sapiens OX=9606 GN=C16orf70'
                         ' PE=1 SV=1',
                         qresult.id)
        self.assertEqual(422, qresult.seq_len)
        self.assertEqual(nhits, len(qresult))

        hit = qresult[0]
        self.assertEqual('PF03676.14_1', hit.id)
        self.assertEqual('UPF0183 ; Uncharacterised protein family (UPF0183)', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(9.9e-102, hit.evalue)
        self.assertEqual(792.76, hit.score)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
        self.assertTrue(hsp.is_included)
        self.assertEqual(9.9e-102, hsp.evalue)
        self.assertEqual(792.76, hsp.score)
        self.assertEqual(1, hsp.hit_start)
        self.assertEqual(394, hsp.hit_end)
        self.assertEqual(22, hsp.query_start)
        self.assertEqual(407, hsp.query_end)
        self.assertEqual('GMHFSQSVAIIQSQVGTIRGVQVLYSDQNPLSVDLVINMPQDGMRLIFDPVAQRLKIIEIYNMKLVKLRYSGMCFNSPEI'
                         'TPSIEQVEHCFGATHPGLYDSQRHLFALNFRGLSFYFPVDS-----KFEPGYAHGLGSLQFPNGGSPVVSRTTIYYGSQH'
                         'QLSSNTSSRVSGVPLPDLPLSCYRQQLHLRRCDVLRNTTSTMGLRLHMFTEGT--SRALEPSQVALVRVVRFGDSCQGVA'
                         'RALGAPARLYYKADDKMRIHRPTARRR-PPPASDYLFNYFTLGLDVLFDARTNQVKKFVLHTNYPGHYNFNMYHRCEFEL'
                         'TVQPD-KSEAHSLVESGGGVAVTAYSKWEVVSRAL-RVCERPVVLNRASSTNTTNPFGSTFCYGYQDIIFEVMSNNYIAS'
                         'ITLY', str(hsp.hit.seq))
        self.assertEqual('GMPLAQAVAILQKHCRIIKNVQVLYSEQSPLSHDLILNLTQDGIKLMFDAFNQRLKVIEVCDLTKVKLKYCGVHFNSQAI'
                         'APTIEQIDQSFGATHPGVYNSAEQLFHLNFRGLSFSFQLDSWTEAPKYEPNFAHGLASLQIPHGA--TVKRMYIYSGNSL'
                         'Q---------DTKA-PMMPLSCFLGNVYAESVDVLRDGTGPAGLRLRLLAAGCGPGLLADAKMRVFERSVYFGDSCQDVL'
                         'SMLGSPHKVFYKSEDKMKIHSPSPHKQVPSKCNDYFFNYFTLGVDILFDANTHKVKKFVLHTNYPGHYNFNIYHRCEFKI'
                         'PLAIKKENADG------QTETCTTYSKWDNIQELLGHPVEKPVVLHRSSSPNNTNPFGSTFCFGLQRMIFEVMQNNHIAS'
                         'VTLY', str(hsp.query.seq))

        # Check last hit
        hit = qresult[nhits - 1]
        self.assertEqual('PF07467.11_4', hit.id)
        self.assertEqual('BLIP ; Beta-lactamase inhibitor (BLIP)', hit.description)
        self.assertTrue(hit.is_included)
        self.assertEqual(3.9e+02, hit.evalue)
        self.assertEqual(22.84, hit.score)
        self.assertEqual(1, len(hit))

        hsp = hit.hsps[0]
        self.assertTrue(hsp.is_included)
        self.assertEqual(3.9e+02, hsp.evalue)
        self.assertEqual(22.84, hsp.score)
        self.assertEqual(8, hsp.hit_start)
        self.assertEqual(96, hsp.hit_end)
        self.assertEqual(19, hsp.query_start)
        self.assertEqual(114, hsp.query_end)
        self.assertEqual('FTLGMPLAQAVAILQKHCRIIKNVQVLYSEQSPLSHDLILNLTQDGIKLMFDAFNQRLKVIEVCDLTKVKLKYCGVH-FN'
                         'SQAIAPTIEQIDQSFGA', str(hsp.query.seq))
        self.assertEqual('IQFGMDRTLVWQLAGADQSCSDQVERIICYNNPDH-------YGPQGHFFFNA-ADKLIHKRQMELFPAPKPTMRLATYN'
                         'KTQTGMTEAQFWAAVPS', str(hsp.hit.seq))


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    unittest.main(testRunner=runner)
