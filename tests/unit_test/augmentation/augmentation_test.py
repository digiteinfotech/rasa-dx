from augmentation.paraphrase.paraphrasing import ParaPhrasing
from augmentation.knowledge_graph.document_parser import DocumentParser
from augmentation.knowledge_graph.training_data_generator import TrainingDataGenerator
pdf_file = "./tests/testing_data/file_data/sample1.pdf"
docx_file = "./tests/testing_data/file_data/sample1.docx"

class TestQuestionGeneration:

    def test_generate_questions(self):
        expected = ['Where is digite located?',
                    'Where is digite?',
                    'What is the location of digite?',
                    'Where is the digite located?',
                    'Where is it located?',
                    'What location is digite located?',
                    'Where is the digite?',
                    'where is digite located?',
                    'Where is digite situated?',
                    'digite is located where?']
        actual = ParaPhrasing.paraphrases('where is digite located?')
        assert any(text in expected for text in actual)

    def test_generate_questions_token(self):
        expected = ['A friend.',
                    'A friend of mine.',
                    'a friend',
                    'My friend.',
                    'I have a friend.',
                    'A friend',
                    'A friend to me.',
                    'A good friend.',
                    'Person of interest, friend.',
                    'The friend.']
        actual = ParaPhrasing.paraphrases('friend')
        assert any(text in expected for text in actual)

    def test_generate_questions_token_special(self):
        expected = ['A friend!',
                    "I'm a friend!",
                    'I am a friend!',
                    'My friend!',
                    "It's a friend!",
                    "That's a friend!",
                    'Someone is a friend!',
                    'You are a friend!',
                    "I'm your friend!",
                    "I'm a friend."]

        actual = ParaPhrasing.paraphrases('friend! @#.')
        assert any(text in expected for text in actual)

class TestFileData:

    def test_doc_structure_pdf(self):
        structure, list_sentences = DocumentParser.parse(pdf_file)
        assert structure[31] == [32]
        assert list_sentences[0] == '<h1> 1 Introducing  ONEPOINT Projects'
        final_list = TrainingDataGenerator.generate_intent(structure, list_sentences)
        expected = ['root_1-Introducing--ONEPOINT-Projects_1.3-Basic-Concepts_1.3.8-Open-Design']
        assert any(item.intent in expected for item in final_list)

    def test_doc_structure_docx(self):
        structure, list_sentences = DocumentParser.parse(docx_file)
        assert structure[23] == [24, 25]
        assert list_sentences[0] == '<h0> Demonstration of DOCX support in calibre'
        final_list = TrainingDataGenerator.generate_intent(structure, list_sentences)
        expected = ['root_Demonstration-of-DOCX-support-in-calibre']
        assert any(item.intent in expected for item in final_list)