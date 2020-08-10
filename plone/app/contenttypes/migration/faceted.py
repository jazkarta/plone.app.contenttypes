from zope.component import adapter
from zope.interface import alsoProvides
from zope.interface import implementer
from zope.interface import Interface

from plone.app.contenttypes.migration.migration import ICustomMigrator

from eea.facetednavigation.criteria.handler import Criteria
from eea.facetednavigation.criteria.interfaces import ICriteria
from eea.facetednavigation.indexes.language.interfaces import ILanguageWidgetAdapter
from eea.facetednavigation.interfaces import IFacetedNavigable
from eea.facetednavigation.layout.interfaces import IFacetedLayout
from eea.facetednavigation.settings.interfaces import IDisableSmartFacets
from eea.facetednavigation.settings.interfaces import IHidePloneLeftColumn
from eea.facetednavigation.settings.interfaces import IHidePloneRightColumn
from eea.facetednavigation.subtypes.interfaces import IFacetedWrapper
from eea.facetednavigation.views.interfaces import IViewsInfo
from eea.facetednavigation.widgets.alphabetic.interfaces import IAlphabeticWidget
from eea.facetednavigation.widgets.interfaces import ICriterion
from eea.facetednavigation.widgets.interfaces import IWidget
from eea.facetednavigation.widgets.interfaces import IWidgetsInfo
from eea.facetednavigation.widgets.resultsfilter.interfaces import IResultsFilterWidget

import logging


logger = logging.getLogger(__name__)


@implementer(ICustomMigrator)
@adapter(Interface)
class FacetedNavigationMigrator(object):

    def __init__(self, context):
        self.context = context

    def migrate(self, old, new):
        if IFacetedNavigable.providedBy(old):
            logger.info("Migrating faceted navigation criteria for: %s" % new.absolute_url_path())
            criteria = Criteria(new)
            criteria._update(ICriteria(old).criteria)

            IFacetedLayout(new).update_layout('listing_view')

        interfaces = [
            IFacetedNavigable,
            IDisableSmartFacets,
            IHidePloneLeftColumn,
            IHidePloneRightColumn,
            ICriteria,
            ILanguageWidgetAdapter,
            IFacetedWrapper,
            IViewsInfo,
            IAlphabeticWidget,
            ICriterion,
            IWidget,
            IWidgetsInfo,
            IResultsFilterWidget,
        ]

        for interface in interfaces:
            if interface.providedBy(old):
                alsoProvides(new, interface)
