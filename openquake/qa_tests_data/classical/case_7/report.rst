Classical Hazard QA Test, Case 7
================================

============== ===================
checksum32     359,954,679        
date           2018-10-05T03:05:08
engine_version 3.3.0-git48e9a474fd
============== ===================

num_sites = 1, num_levels = 3

Parameters
----------
=============================== ==================
calculation_mode                'classical'       
number_of_logic_tree_samples    0                 
maximum_distance                {'default': 200.0}
investigation_time              1.0               
ses_per_logic_tree_path         1                 
truncation_level                0.0               
rupture_mesh_spacing            0.1               
complex_fault_mesh_spacing      0.1               
width_of_mfd_bin                1.0               
area_source_discretization      10.0              
ground_motion_correlation_model None              
minimum_intensity               {}                
random_seed                     1066              
master_seed                     0                 
ses_seed                        42                
=============================== ==================

Input files
-----------
======================= ============================================================
Name                    File                                                        
======================= ============================================================
gsim_logic_tree         `gsim_logic_tree.xml <gsim_logic_tree.xml>`_                
job_ini                 `job.ini <job.ini>`_                                        
source                  `source_model_1.xml <source_model_1.xml>`_                  
source                  `source_model_2.xml <source_model_2.xml>`_                  
source_model_logic_tree `source_model_logic_tree.xml <source_model_logic_tree.xml>`_
======================= ============================================================

Composite source model
----------------------
========= ======= =============== ================
smlt_path weight  gsim_logic_tree num_realizations
========= ======= =============== ================
b1        0.70000 trivial(1)      1/1             
b2        0.30000 trivial(1)      1/1             
========= ======= =============== ================

Required parameters per tectonic region type
--------------------------------------------
====== ================ ========= ========== ==========
grp_id gsims            distances siteparams ruptparams
====== ================ ========= ========== ==========
0      SadighEtAl1997() rrup      vs30       mag rake  
1      SadighEtAl1997() rrup      vs30       mag rake  
====== ================ ========= ========== ==========

Realizations per (TRT, GSIM)
----------------------------

::

  <RlzsAssoc(size=2, rlzs=2)
  0,SadighEtAl1997(): [0]
  1,SadighEtAl1997(): [1]>

Number of ruptures per tectonic region type
-------------------------------------------
================== ====== ==================== ============ ============
source_model       grp_id trt                  eff_ruptures tot_ruptures
================== ====== ==================== ============ ============
source_model_1.xml 0      Active Shallow Crust 140          140         
source_model_2.xml 1      Active Shallow Crust 91           91          
================== ====== ==================== ============ ============

============= ===
#TRT models   2  
#eff_ruptures 231
#tot_ruptures 231
#tot_weight   287
============= ===

Slowest sources
---------------
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= ======
grp_id source_id code gidx1 gidx2 num_ruptures calc_time split_time num_sites num_split weight
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= ======
0      1         S    0     2     91           0.0       2.575E-05  0.0       1         0.0   
0      2         C    2     8     49           0.0       1.144E-05  0.0       1         0.0   
1      1         S    0     2     91           0.0       1.049E-05  0.0       1         0.0   
====== ========= ==== ===== ===== ============ ========= ========== ========= ========= ======

Computation times by source typology
------------------------------------
==== ========= ======
code calc_time counts
==== ========= ======
C    0.0       1     
S    0.0       2     
==== ========= ======

Duplicated sources
------------------
========= ========= ========
source_id calc_time num_dupl
========= ========= ========
1         0.0       2       
========= ========= ========
Total time in duplicated sources: 0/0 (76%)

Information about the tasks
---------------------------
================== ======= ======= ======= ======= =======
operation-duration mean    stddev  min     max     outputs
read_source_models 0.08061 0.07184 0.02981 0.13141 2      
split_filter       0.00474 NaN     0.00474 0.00474 1      
================== ======= ======= ======= ======= =======

Data transfer
-------------
================== ====================================================================== ========
task               sent                                                                   received
read_source_models monitor=662 B converter=638 B fnames=366 B                             3.47 KB 
split_filter       srcs=1.9 KB monitor=343 B srcfilter=253 B sample_factor=21 B seed=15 B 2.08 KB 
================== ====================================================================== ========

Slowest operations
------------------
======================== ======== ========= ======
operation                time_sec memory_mb counts
======================== ======== ========= ======
total read_source_models 0.16123  0.26172   2     
updating source_info     0.00989  0.0       1     
total split_filter       0.00474  0.0       1     
======================== ======== ========= ======