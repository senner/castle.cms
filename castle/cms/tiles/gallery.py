from castle.cms import defaults
from castle.cms.tiles.base import BaseImagesTile
from castle.cms.tiles.base import DisplayTypeTileMixin
from castle.cms.tiles.content import IImagesTileSchema
from castle.cms.tiles.views import BaseTileView
from castle.cms.tiles.views import TileViewsSource
from castle.cms.widgets import PreviewSelectFieldWidget
from plone.autoform import directives as form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary


class DefaultView(BaseTileView):
    name = 'default'
    order = 0
    index = ViewPageTemplateFile('templates/gallery/default.pt')
    tile_name = 'gallery'


class GalleryTile(BaseImagesTile, DisplayTypeTileMixin):
    display_type_name = 'gallery'
    display_type_default = 'default'
    display_type_fallback_view = DefaultView

    render = DisplayTypeTileMixin.render_display

    @property
    def gallery_height(self):
        return self.data.get('gallery_height', 'default')


class IGalleryTileSchema(IImagesTileSchema):

    form.widget('display_type', PreviewSelectFieldWidget,
                tile_name='gallery')
    display_type = schema.Choice(
        title=u"Display Type",
        source=TileViewsSource('gallery'),
        default=defaults.get('gallery_tile_displaytype', u'default')
    )

    gallery_height = schema.Choice(
        title=u"Gallery Height",
        default='default',
        vocabulary=SimpleVocabulary([
            SimpleVocabulary.createTerm('small', 'small', 'Small'),
            SimpleVocabulary.createTerm('default', 'default', 'Default'),
            SimpleVocabulary.createTerm('large', 'large', 'Large'),
            SimpleVocabulary.createTerm('x-large', 'x-large', 'X-Large')
        ])
    )
