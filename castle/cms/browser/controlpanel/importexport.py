from castle.cms.interfaces import IImportExportConfiguration
from collective.elasticsearch.es import ElasticSearchCatalog
from elasticsearch import TransportError
from plone import api
from plone.app.registry.browser import controlpanel
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.annotation.interfaces import IAnnotations
from castle.cms._scripts.export_content import run_export
from castle.cms._scripts.importjson import CastleImporter

import csv
from z3c.form import button
import copy
import os
import sys

ROOT_DIR = os.path.abspath(os.curdir)
exFold = os.path.join(ROOT_DIR, 'castle/cms/exportresults')
exist = False

class ImportExportControlPanelForm(controlpanel.RegistryEditForm):
    schema_prefix = 'castle'
    schema = IImportExportConfiguration
    id = "ImportExportControlPanel"
    label = u"Site Import/Export Configuration"
    buttons = controlpanel.RegistryEditForm.buttons.copy()

    import pdb; pdb.set_trace()

    @button.buttonAndHandler(u'Import')
    def Import(self, action):
        print("import")
        data, errors = self.extractData()

        imPath = str(data["import_path"])
        #import pdb; pdb.set_trace()
        importer = CastleImporter()
        importer.import_object(filepath=imPath, container=api.portal.get())
        print(importer.imported_count)


    @button.buttonAndHandler(u'Export')
    def export(self, action):
        print("export")
        data, errors = self.extractData()

        # exFold = str(data["export_folder"])

        # if exFold == None or exFold == 'None':
        #     exFold = os.path.expanduser('~/Downloads')
        # else:
        #     exFold = os.path.normpath(exFold)
        
        catalog = api.portal.get_tool(name='portal_catalog')
        # if args.createdsince:
        #     print('exporting items created since %s' % args.createdsince)
        #     date_range = {
        #         'query': (
        #             DateTime(args.createdsince),
        #             DateTime('2062-05-08 23:59:59'),
        #         ),
        #         'range': 'min:max'
        #     }
        #     query = catalog(created=date_range)
        # elif args.modifiedsince:
        #     print('exporting items modified since %s' % args.modifiedsince)
        #     date_range = {
        #         'query': (
        #             DateTime(args.modifiedsince),
        #             DateTime('2062-05-08 23:59:59'),
        #         ),
        #         'range': 'min:max'
        #     }
        #     query = catalog(modified=date_range)
        #else:
        query = catalog()
        run_export(query, exportfolder=exFold)
        super(ImportExportControlPanelForm, self)
    

    @button.buttonAndHandler((u"Download"), condition=lambda form: exist)
    def Download(self, action):
        print("download export")
        

class ImportExportControlPanel(controlpanel.ControlPanelFormWrapper):
    form = ImportExportControlPanelForm
    index = ViewPageTemplateFile('templates/import-export.pt')
    
    exist = len(os.listdir(exFold))>0
    import pdb; pdb.set_trace()
    # def update(self):
    #     # Hide form buttons
    #     self.form.buttons = copy.deepcopy(self.form.buttons)
    #     del self.form.buttons['save']
    #     del self.form.buttons['cancel']
    #     super(ImportExportControlPanel, self).update()
    #     # Create immutable copy which you can manipulate
        

    #     # Remove button using dictionary style delete
    #     # import pdb; pdb.set_trace()

        
    def updateActions(self):
        super(ImportExportControlPanel, self).updateActions()
        del self.form.buttons['save']
        del self.form.buttons['cancel']
        # self.actions['save'].addClass("btn btn-primary")
        # self.actions['cancel'].addClass("btn btn-secondary")

