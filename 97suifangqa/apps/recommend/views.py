# -*- coding: utf-8 -*-

"""
views for apps/recommend
"""

import itertools
try:
    import json
except ImportError:
    from django.utils import simplejson as json

from django.http import (
        HttpResponse, HttpResponseRedirect,
        HttpResponseForbidden, Http404
)
from django.views.defaults import permission_denied
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from recommend import models as rm
from sciblog.models import SciBlog
from tools import make_tag, get_research_config, make_config_display


# index {{{
def recommend_index(request):
    """
    index view for apps/recommend
    """
    template_name = 'recommend/recommend_index.html'
    blogs = SciBlog.objects.all().order_by('id')
    blog_list = []
    for blog in blogs:
        if blog.research_configs.all():
            has_info = True
        else:
            has_info = False
        b = {
            'id': blog.id,
            'title': blog.title,
            'has_info': has_info,
        }
        blog_list.append(b)
    #
    context = {
        'blog_list': blog_list,
    }
    return render(request, template_name, context)
# }}}


# add_edit_blog_info {{{
@login_required
def add_edit_blog_info(request, blog_id=None):
    """
    add/edit the infomation (used to recommend blog for user)
    of the given blog

    ONLY *STAFF* ALLOWED
    """
    template_name = 'recommend/add_edit_blog_info.html'
    template_name_error = 'recommend/add_edit_blog_info_error.html'
    context_error = {
        'no_indicator': False,
        'no_indicator_atom': False,
        'no_treat_response': False,
        'ResearchIndicatorName': rm.ResearchIndicator._meta.verbose_name_plural,
        'ResearchAtomName': rm.ResearchAtom._meta.verbose_name_plural,
        'TreatResponseName': rm.TreatResponse._meta.verbose_name_plural,
    }
    # check user type
    if not request.user.is_staff:
        #return permission_denied(request)
        html = """
            <h1>403 Forbidden</h1>
            <h2>ONLY *STAFF* ALLOWED</h2>
        """
        return HttpResponseForbidden(html)
    ## blog object
    try:
        blog_id = int(blog_id)
        blog_obj = get_object_or_404(SciBlog, id=blog_id)
    except ValueError:
        raise ValueError(u"Error: blog_id='%s'错误" % blog_id)
    except SciBlog.DoesNotExist:
        raise ValueError(u"Error: SciBlog id='%s'不存在" % blog_id)
    context_error['blog'] = blog_obj
    ## research indicators & check
    r_indicators = blog_obj.research_indicators.all()
    r_indicators_id = [ri.id for ri in r_indicators]
    rind_num = len(r_indicators)
    # check indicator
    if rind_num == 0:
        context_error['no_indicator'] = True
        return render(request, template_name_error, context_error)
    # check indicator research atoms
    no_atom_ri = []
    for ri in r_indicators:
        if not ri.research_atoms.all():
            context_error['no_indicator_atom'] = True
            no_atom_ri.append({
                'id': ri.id,
                'display': ri.__unicode__(),
            })
    #
    if context_error['no_indicator_atom']:
        context_error['no_atom_ri'] = no_atom_ri
        return render(request, template_name_error, context_error)
    # treat response & check
    treat_responses = rm.TreatResponse.objects.all()
    if not treat_responses:
        context_error['no_treat_response'] = True
        return render(request, template_name_error, context_error)
    else:
        treat_responses_list = [tr.dump() for tr in treat_responses]
        treat_responses_objs = {'name': rm.TreatResponse._meta.verbose_name_plural}
        for tr in treat_responses:
            id = tr.id
            treat_responses_objs['id%s'%id] = tr.dump()
    ## research indicator numbers (categories by number)
    rind_categories = {}
    for i in range(1, rind_num+1):
        comb = list(itertools.combinations(r_indicators_id, i))
        # tag all combinations
        comb_tagged = []
        for c in comb:
            tag = make_tag(ids=c, tag='comb')
            comb_tagged.append({'tag': tag, 'data': c})
        rind_categories['N%s'%i] = comb_tagged
    # dump used research indicators
    rind_objs = {}
    for id in r_indicators_id:
        ri_obj = get_object_or_404(rm.ResearchIndicator, id=id)
        ri_data = ri_obj.dump()
        # atoms
        ri_data['atoms_id'] = [atom.id
                for atom in ri_obj.research_atoms.all()]
        rind_objs['id%s'%id] = ri_data
    ## research configs
    rind_combs = []
    for ric in rind_categories.values():
        rind_combs = rind_combs + ric
    #
    research_configs = {}
    for ric in rind_combs:
        key = ric['tag']
        atoms_id_list = []
        for id in ric['data']:
            atoms_id_list.append(rind_objs['id%s'%id]['atoms_id'])
        # itertools to generate combinations
        configs = list(itertools.product(*atoms_id_list))
        configs_tagged = []
        # generate config data for front page
        for conf in configs:
            config_obj = get_research_config(atoms=conf)
            if config_obj:
                config_data = config_obj.dump()
            else:
                config_data = {}
            tag = make_tag(ids=conf, tag='conf')
            display = make_config_display(atoms=conf)
            config_data.update({
                    'tag': tag,
                    'data': conf,
                    'display': display,
            })
            configs_tagged.append(config_data)
        # TODO
        data = {
            'rind_ids': list(ric['data']),
            'configs': configs_tagged,
        }
        research_configs[key] = data
    ## context
    context = {
        'blog': blog_obj,
        'rind_num': rind_num,
        'rind_objs_json': json.dumps(rind_objs),
        'rind_combs_json': json.dumps(rind_combs),
        'rind_categories_json': json.dumps(rind_categories),
        'research_configs_json': json.dumps(research_configs),
        'treat_responses_list_json': json.dumps(treat_responses_list),
        'treat_responses_objs_json': json.dumps(treat_responses_objs),
    }
    return render(request, template_name, context)
# }}}


# ajax add_edit_configs {{{
@login_required
def ajax_add_edit_configs(request):
    """
    response to the ajax post configs data
    """
    data = {'failed': True}
    if request.is_ajax() and request.method == 'POST':
        #print request.POST.dict()
        configs_list = json.loads(request.POST.get('configs_list'))
        blog_id = int(request.POST.get('blog_id'))
        blog_obj = get_object_or_404(SciBlog, id=blog_id)
        #print configs_list
        for conf in configs_list:
            if conf['action'] == 'add':
                # add config
                tr_obj = get_object_or_404(rm.TreatResponse,
                        id=conf['treatResponse_id'])
                new_conf_obj = rm.ResearchConfig.objects.create(
                        blog=blog_obj, treatResponse=tr_obj,
                        weight=conf['weight'])
                new_conf_obj.save()
                # add m2m researchAtoms
                for atom_id in conf['data']:
                    atom_obj = get_object_or_404(rm.ResearchAtom,
                            id=atom_id)
                    new_conf_obj.researchAtoms.add(atom_obj)
                new_conf_obj.save()
            elif conf['action'] == 'delete':
                # delete config
                conf_obj = get_object_or_404(rm.ResearchConfig,
                        id=conf['id'])
                conf_obj.delete()
            elif conf['action'] == 'edit':
                # edit config
                conf_obj = get_object_or_404(rm.ResearchConfig,
                        id=conf['id'])
                conf_obj.weight = conf['weight']
                tr_obj = get_object_or_404(rm.TreatResponse,
                        id=conf['treatResponse_id'])
                conf_obj.treatResponse = tr_obj
                conf_obj.save()
            else:
                # action==None / unknown action
                pass
        data = {'failed': False}
    #
    return HttpResponse(json.dumps(data), mimetype='application/json')
# }}}


