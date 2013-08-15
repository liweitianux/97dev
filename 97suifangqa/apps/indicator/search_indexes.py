# -*- coding: utf-8 -*-

from haystack import indexes

from indicator import models as im



# IndicatorCategoryIndex {{{
class IndicatorCategoryIndex(indexes.SearchIndex, indexes.Indexable):
    """
    search index for 'Indicator'
    """
    text = indexes.CharField(document=True, use_template=True)
    addByUser = indexes.CharField(model_attr='addByUser')

    def get_model(self):
        return im.IndicatorCategory

    def index_queryset(self, using=None):
        """
        used when the entire index for model is updated
        """
        return self.get_model().objects.all()
# }}}


# IndicatorIndex {{{
class IndicatorIndex(indexes.SearchIndex, indexes.Indexable):
    """
    search index for 'Indicator'
    """
    text = indexes.CharField(document=True, use_template=True)
    addByUser = indexes.CharField(model_attr='addByUser')
    dataType = indexes.CharField(model_attr='dataType')
    categories_id = indexes.MultiValueField()

    def get_model(self):
        return im.Indicator

    def prepare_categories(self, obj):
        return [c.id for c in obj.categories.all()]

    def index_queryset(self, using=None):
        """
        used when the entire index for model is updated
        """
        return self.get_model().objects.all()
# }}}



# vim: set ts=4 sw=4 tw=0 fenc=utf-8 ft=python: 
