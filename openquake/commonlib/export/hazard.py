#  -*- coding: utf-8 -*-
#  vim: tabstop=4 shiftwidth=4 softtabstop=4

#  Copyright (c) 2014, GEM Foundation

#  OpenQuake is free software: you can redistribute it and/or modify it
#  under the terms of the GNU Affero General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  OpenQuake is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with OpenQuake.  If not, see <http://www.gnu.org/licenses/>.

import os
import collections

import numpy

from openquake.commonlib.export import export
from openquake.commonlib.writers import (
    scientificformat, floatformat, save_csv)
from openquake.commonlib import hazard_writers
from openquake.hazardlib.imt import from_string


# #################### export Ground Motion fields ########################## #

class GmfSet(object):
    """
    Small wrapper around the list of Gmf objects associated to the given SES.
    """
    def __init__(self, gmfset):
        self.gmfset = gmfset
        self.investigation_time = None
        self.stochastic_event_set_id = 1

    def __iter__(self):
        return iter(self.gmfset)

    def __nonzero__(self):
        return bool(self.gmfset)

    def __str__(self):
        return (
            'GMFsPerSES(investigation_time=%f, '
            'stochastic_event_set_id=%s,\n%s)' % (
                self.investigation_time,
                self.stochastic_event_set_id, '\n'.join(
                    sorted(str(g) for g in self.gmfset))))


class GroundMotionField(object):
    """
    The Ground Motion Field generated by the given rupture
    """
    def __init__(self, imt, sa_period, sa_damping, rupture_id, gmf_nodes):
        self.imt = imt
        self.sa_period = sa_period
        self.sa_damping = sa_damping
        self.rupture_id = rupture_id
        self.gmf_nodes = gmf_nodes

    def __iter__(self):
        return iter(self.gmf_nodes)

    def __getitem__(self, key):
        return self.gmf_nodes[key]

    def __str__(self):
        # string representation of a _GroundMotionField object showing the
        # content of the nodes (lon, lat an gmv). This is useful for debugging
        # and testing.
        mdata = ('imt=%(imt)s sa_period=%(sa_period)s '
                 'sa_damping=%(sa_damping)s rupture_id=%(rupture_id)s' %
                 vars(self))
        nodes = sorted(map(str, self.gmf_nodes))
        return 'GMF(%s\n%s)' % (mdata, '\n'.join(nodes))


class GroundMotionFieldNode(object):
    # the signature is not (gmv, x, y) because the XML writer expects
    # a location object
    def __init__(self, gmv, loc):
        self.gmv = gmv
        self.location = loc

    def __lt__(self, other):
        """
        A reproducible ordering by lon and lat; used in
        :function:`openquake.commonlib.hazard_writers.gen_gmfs`
        """
        return (self.location.x, self.location.y) < (
            other.location.x, other.location.y)

    def __str__(self):
        """Return lon, lat and gmv of the node in a compact string form"""
        return '<X=%9.5f, Y=%9.5f, GMV=%9.7f>' % (
            self.location.x, self.location.y, self.gmv)


class GmfCollection(object):
    """
    Object converting the parameters

    :param sitecol: SiteCollection
    :rupture_tags: tags of the ruptures
    :gmfs_by_imt: dictionary of GMFs by IMT

    into an object with the right form for the EventBasedGMFXMLWriter.
    Iterating over a GmfCollection yields GmfSet objects.
    """
    def __init__(self, sitecol, rupture_tags, gmfs_by_imt):
        self.sitecol = sitecol
        self.rupture_tags = rupture_tags
        self.gmfs_by_imt = gmfs_by_imt

    def __iter__(self):
        gmfset = []
        for imt_str, gmfs in sorted(self.gmfs_by_imt.iteritems()):
            imt, sa_period, sa_damping = from_string(imt_str)
            for rupture_tag, gmf in zip(self.rupture_tags, gmfs.transpose()):
                nodes = (GroundMotionFieldNode(gmv, site.location)
                         for site, gmv in zip(self.sitecol, gmf))
                gmfset.append(
                    GroundMotionField(
                        imt, sa_period, sa_damping, rupture_tag, nodes))
        yield GmfSet(gmfset)


@export.add(('gmf', 'xml'))
def export_gmf_xml(key, export_dir, fname, sitecol, rupture_tags, gmfs):
    """
    :param key: output_type and export_type
    :param export_dir: the directory where to export
    :param fname: name of the exported file
    :param sitecol: site collection
    :rupture_tags: a list of rupture tags
    :gmfs: a dictionary of ground motion fields keyed by IMT
    """
    dest = os.path.join(export_dir, fname)
    writer = hazard_writers.EventBasedGMFXMLWriter(
        dest, sm_lt_path='', gsim_lt_path='')
    with floatformat('%12.8E'):
        writer.serialize(GmfCollection(sitecol, rupture_tags, gmfs))
    return {key: dest}


@export.add(('gmf', 'csv'))
def export_gmf_csv(key, export_dir, fname, sitecol, rupture_tags, gmfs):
    """
    :param key: output_type and export_type
    :param export_dir: the directory where to export
    :param fname: name of the exported file
    :param sitecol: site collection
    :rupture_tags: a list of rupture tags
    :gmfs: a dictionary of ground motion fields keyed by IMT
    """
    dest = os.path.join(export_dir, fname)
    with floatformat('%12.8E'), open(dest, 'w') as f:
        for imt, gmf in gmfs.iteritems():
            for site, gmvs in zip(sitecol, gmf):
                row = [imt, site.location.x, site.location.y] + list(gmvs)
                f.write(scientificformat(row) + '\n')
    return {key: dest}

# ####################### export hazard curves ############################ #

HazardCurve = collections.namedtuple('HazardCurve', 'location poes')


@export.add(('hazard_curves', 'csv'))
def export_hazard_curves_csv(key, export_dir, fname, sitecol, curves_by_imt,
                             imtls, investigation_time=None):
    """
    Export the curves of the given realization into XML.

    :param key: output_type and export_type
    :param export_dir: the directory where to export
    :param fname: name of the exported file
    :param sitecol: site collection
    :param curves_by_imt: dictionary with the curves keyed by IMT
    """
    dest = os.path.join(export_dir, fname)
    rows = []
    for imt in sorted(curves_by_imt):
        row = map(scientificformat, curves_by_imt[imt])
        rows.append(row)
    save_csv(dest, numpy.array(rows).T)
    return {fname: dest}


@export.add(('hazard_curves', 'xml'))
def export_hazard_curves_xml(key, export_dir, fname, sitecol, curves_by_imt,
                             imtls, investigation_time):
    """
    Export the curves of the given realization into XML.

    :param key: output_type and export_type
    :param export_dir: the directory where to export
    :param fname: name of the exported file
    :param sitecol: site collection
    :param rlz: realization instance
    :param curves_by_imt: dictionary with the curves keyed by IMT
    :param imtls: dictionary with the intensity measure types and levels
    :param investigation_time: investigation time in years
    """
    mdata = []
    hcurves = []
    for imt_str, imls in sorted(imtls.iteritems()):
        hcurves.append(
            [HazardCurve(site.location, poes)
             for site, poes in zip(sitecol, curves_by_imt[imt_str])])
        imt = from_string(imt_str)
        mdata.append({
            'quantile_value': None,
            'statistics': None,
            'smlt_path': '',
            'gsimlt_path': '',
            'investigation_time': investigation_time,
            'imt': imt[0],
            'sa_period': imt[1],
            'sa_damping': imt[2],
            'imls': imls,
        })
    dest = os.path.join(export_dir, fname)
    writer = hazard_writers.MultiHazardCurveXMLWriter(dest, mdata)
    with floatformat('%12.8E'):
        writer.serialize(hcurves)
    return {fname: dest}


@export.add(('hazard_stats', 'csv'))
def export_stats_csv(key, export_dir, fname, sitecol, data_by_imt):
    """
    Export the scalar outputs.

    :param key: output_type and export_type
    :param export_dir: the directory where to export
    :param fname: file name
    :param sitecol: site collection
    :param data_by_imt: dictionary of floats keyed by IMT
    """
    dest = os.path.join(export_dir, fname)
    rows = []
    for imt in sorted(data_by_imt):
        row = [imt]
        for col in data_by_imt[imt]:
            row.append(scientificformat(col))
        rows.append(row)
    save_csv(dest, numpy.array(rows).T)
    return {fname: dest}


@export.add(('uhs', 'csv'))
def export_uhs_csv(key, export_dir, fname, sitecol, hmaps):
    """
    Export the scalar outputs.

    :param key: output_type and export_type
    :param export_dir: the directory where to export
    :param fname: file name
    :param sitecol: site collection
    :param hmaps:
        an array N x I x P where N is the number of sites,
        I the number of IMTs of SA type, and P the number of poes
    """
    dest = os.path.join(export_dir, fname)
    rows = ([[lon, lat]] + list(row)
            for lon, lat, row in zip(sitecol.lons, sitecol.lats, hmaps))
    save_csv(dest, rows)
    return {fname: dest}
