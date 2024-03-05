import unittest
from datetime import date
from time import sleep

from omaslib.src.connection import Connection
from omaslib.src.helpers.context import Context
from omaslib.src.helpers.datatypes import NamespaceIRI, QName, NCName, AnyIRI
from omaslib.src.helpers.langstring import LangString
from omaslib.src.project import Project


class Testproject(unittest.TestCase):
    _connection: Connection
    _unpriv: Connection

    @classmethod
    def setUpClass(cls):
        cls._context = Context(name="DEFAULT")

        cls._connection = Connection(server='http://localhost:7200',
                                     repo="omas",
                                     userId="rosenth",
                                     credentials="RioGrande",
                                     context_name="DEFAULT")
        cls._unpriv = Connection(server='http://localhost:7200',
                                 repo="omas",
                                 userId="fornaro",
                                 credentials="RioGrande",
                                 context_name="DEFAULT")


        # cls._connection.clear_graph(QName('test:shacl'))
        # cls._connection.clear_graph(QName('test:onto'))
        # cls._connection.upload_turtle("omaslib/testdata/connection_test.trig")
        # sleep(1)  # upload may take a while...

    @classmethod
    def tearDownClass(cls):
        cls._connection.clear_graph(QName('omas:admin'))
        cls._connection.upload_turtle("omaslib/ontologies/admin.trig")
        sleep(1)  # upload may take a while...

    def test_project_read(self):
        project = Project.read(con=self._connection, projectIri=QName("omas:SystemProject"))
        self.assertEqual(NCName("system"), project.projectShortName)
        self.assertEqual(LangString(["System@en",
                                     "System@de",
                                     "Système@fr",
                                     "Systema@it"]), project.label)
        self.assertEqual(NamespaceIRI("http://omas.org/base#"), project.namespaceIri)
        self.assertEqual(LangString(["Project for system administration@en"]), project.comment)
        self.assertEqual(date.fromisoformat("2024-01-01"), project.projectStart)

    @unittest.skip('Work in progress')
    def test_project_search(self):
        projects = Project.search(con=self._connection)
        print("\n------>\n", projects)
        self.assertEqual( ["omas:SystemProject",
                           "omas:HyperHamlet",
                           "http://www.salsah.org/version/2.0/SwissBritNet",
                           "urn:uuid:e184e01e-d40a-4cb8-ab6f-a5c14a7770dd"], projects)

    def test_project_create(self):
        project = Project(con=self._connection,
                          projectShortName="unittest",
                          label=LangString(["unittest@en", "unittest@de"]),
                          namespaceIri=NamespaceIRI("http://unitest.org/project/unittest#"),
                          comment=LangString(["For testing@en", "Für Tests@de"]),
                          projectStart=date(2024, 1, 1),
                          projectEnd=date(2025, 12, 31)
                          )
        project.create()
        projectIri = project.projectIri
        del project

        project2 = Project.read(con=self._connection, projectIri=projectIri)

if __name__ == '__main__':
    unittest.main()
