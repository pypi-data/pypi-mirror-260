import unittest

from pystixview import PySTIXView
from stix2 import Bundle, Relationship
from stix2.parsing import parse

from IPython.display import HTML

import base64
import json
import os

class TestPySTIXView(unittest.TestCase):

    def test_empty_network(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        with open('tests/empty_graph.json', 'r') as fd:
            self.assertEqual(self.graph.to_json(), fd.read())

    def test_empty_network_fail(self):
        with self.assertRaises(ValueError):
            self.graph = PySTIXView("100%", "100%", notebook=False, style="test")

    def test_bundle_string(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        with open('tests/stix_bundle1.json', 'r') as fd:
            self.graph.add_bundle(fd.read())

        with open('tests/bundle1_graph.json', 'r') as fd:
            self.assertEqual(self.graph.to_json(), fd.read())

    def test_bundle_dict(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        with open('tests/stix_bundle1.json', 'r') as fd:
            self.graph.add_bundle(json.loads(fd.read()))

        with open('tests/bundle1_graph.json', 'r') as fd:
            self.assertEqual(self.graph.to_json(), fd.read())

    def test_bundle_object(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        with open('tests/stix_bundle1.json', 'r') as fd:
            bundle = parse(fd.read())
            self.graph.add_bundle(bundle)

        with open('tests/bundle1_graph.json', 'r') as fd:
            self.assertEqual(self.graph.to_json(), fd.read())

    def test_bundle_fail(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        with self.assertRaises(TypeError):
            self.graph.add_bundle(123)

    def test_add_relationship_str(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        with open('tests/stix_bundle2.json', 'r') as fd:
            bundle = parse(fd.read())
        self.graph.add_bundle(bundle)
        relationship = """{
            "type": "relationship",
            "spec_version": "2.1",
            "id": "relationship--d44019b6-b8f7-4cb3-837e-7fd3c5724b87",
            "created": "2020-02-29T18:18:08.661Z",
            "modified": "2020-02-29T18:18:08.661Z",
            "relationship_type": "uses",
            "source_ref": "threat-actor--9a8a0d25-7636-429b-a99e-b2a73cd0f11f",
            "target_ref": "malware--d1c612bc-146f-4b65-b7b0-9a54a14150a4"
        }"""
        self.graph.add_relationship(relationship)
        self.assertTrue( "\"from\": \"threat-actor--9a8a0d25-7636-429b-a99e-b2a73cd0f11f\", \"to\": \"malware--d1c612bc-146f-4b65-b7b0-9a54a14150a4\"" in self.graph.to_json() )

    def test_add_relationship_dict(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        with open('tests/stix_bundle2.json', 'r') as fd:
            bundle = parse(fd.read())
        self.graph.add_bundle(bundle)
        relationship = """{
            "type": "relationship",
            "spec_version": "2.1",
            "id": "relationship--d44019b6-b8f7-4cb3-837e-7fd3c5724b87",
            "created": "2020-02-29T18:18:08.661Z",
            "modified": "2020-02-29T18:18:08.661Z",
            "relationship_type": "uses",
            "source_ref": "threat-actor--9a8a0d25-7636-429b-a99e-b2a73cd0f11f",
            "target_ref": "malware--d1c612bc-146f-4b65-b7b0-9a54a14150a4"
        }"""
        self.graph.add_relationship(json.loads(relationship))
        self.assertTrue( "\"from\": \"threat-actor--9a8a0d25-7636-429b-a99e-b2a73cd0f11f\", \"to\": \"malware--d1c612bc-146f-4b65-b7b0-9a54a14150a4\"" in self.graph.to_json() )

    def test_add_relationship_stix(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        with open('tests/stix_bundle2.json', 'r') as fd:
            bundle = parse(fd.read())
        self.graph.add_bundle(bundle)
        
        relationship = Relationship(relationship_type='uses',
                                    source_ref="threat-actor--9a8a0d25-7636-429b-a99e-b2a73cd0f11f", 
                                    target_ref="malware--d1c612bc-146f-4b65-b7b0-9a54a14150a4")

        self.graph.add_relationship(relationship)
        self.assertTrue( "\"from\": \"threat-actor--9a8a0d25-7636-429b-a99e-b2a73cd0f11f\", \"to\": \"malware--d1c612bc-146f-4b65-b7b0-9a54a14150a4\"" in self.graph.to_json() )

    def test_add_relationship_fail(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        
        with self.assertRaises(TypeError):
            self.graph.add_relationship(123)

    def test_custom_type_fail(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        self.assertRaises(TypeError, self.graph.add_custom_stix_type("x-test"))

    def test_custom_type_icon(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        self.graph.add_custom_stix_type("x-test", node_icon="tests/test-icon.png")
        self.graph.add_node("""
        {
            "type": "x-test",
            "spec_version": "2.1",
            "id": "x-test--45d71d3d-52bd-4300-815a-78c434d4d50c",
            "created": "2024-03-03T15:11:57",
            "modified": "2024-03-03T15:11:57",
            "name": "Test",
            "description": "Test"
        }
        """)
        with open('tests/test-icon.png', 'rb') as fd:
            img_b64 = f"data:image/png;base64,{base64.b64encode(fd.read()).decode('utf-8')}"
            self.assertTrue( img_b64 in self.graph.to_json() )

    def test_custom_type_icon_url(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)

        url = "https://uxwing.com/wp-content/themes/uxwing/download/web-app-development/bug-icon.png"
        self.graph.add_custom_stix_type("x-test", node_icon=url)
        self.graph.add_node("""
        {
            "type": "x-test",
            "spec_version": "2.1",
            "id": "x-test--45d71d3d-52bd-4300-815a-78c434d4d50c",
            "created": "2024-03-03T15:11:57",
            "modified": "2024-03-03T15:11:57",
            "name": "Test",
            "description": "Test"
        }
        """)
        self.assertTrue( url in self.graph.to_json() )

    def test_custom_type_icon_fail(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)

        with self.assertRaises(TypeError):
            self.graph.add_custom_stix_type("x-test", node_icon=123)

        with self.assertRaises(TypeError):
            self.graph.add_custom_stix_type("x-test-2", node_color="test")

    def test_custom_type_fail(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)

        with self.assertRaises(Exception):
            self.graph.add_custom_stix_type("x-test", node_color="#FF0000")
            self.graph.add_custom_stix_type("x-test", node_color="#FF0000")

        
    def test_custom_type_icon_color(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)

        self.graph.add_custom_stix_type("x-test", node_color="#ABCDEF")
        self.graph.add_node("""
        {
            "type": "x-test",
            "spec_version": "2.1",
            "id": "x-test--45d71d3d-52bd-4300-815a-78c434d4d50c",
            "created": "2024-03-03T15:11:57",
            "modified": "2024-03-03T15:11:57",
            "name": "Test",
            "description": "Test"
        }
        """)
        self.assertTrue( "#ABCDEF" in self.graph.to_json() )
        
    def test_node_type(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)

        with self.assertRaises(ValueError):
            self.graph.add_node("""
            {
                "type": "x-test",
                "spec_version": "2.1",
                "id": "x-test--45d71d3d-52bd-4300-815a-78c434d4d50c",
                "created": "2024-03-03T15:11:57",
                "modified": "2024-03-03T15:11:57",
                "name": "Test",
                "description": "Test"
            }
            """)

    def test_add_node_fail(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)
        with self.assertRaises(TypeError):
            self.graph.add_node(123)


    def test_show_graph(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)

        html = self.graph.show_graph(show_physics_buttons=True,
                              show_node_buttons=True,
                              show_edge_buttons=True)
        self.assertTrue( isinstance(html, str))

    def test_show_graph_notebook(self):
        self.graph = PySTIXView("100%", "100%", notebook=True)

        html = self.graph.show_graph(show_physics_buttons=True,
                              show_node_buttons=True,
                              show_edge_buttons=True)
        self.assertTrue( isinstance(html, HTML) )

    def test_save_graph_notebook(self):
        self.graph = PySTIXView("100%", "100%", notebook=False)

        self.graph.save_graph('tests/graph.html', show_physics_buttons=True,
                              show_node_buttons=True,
                              show_edge_buttons=True)


        self.assertTrue( os.path.exists('tests/graph.html') )



