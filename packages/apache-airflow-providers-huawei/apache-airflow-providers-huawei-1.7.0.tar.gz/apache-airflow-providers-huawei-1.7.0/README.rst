
.. Licensed to the Apache Software Foundation (ASF) under one
   or more contributor license agreements.  See the NOTICE file
   distributed with this work for additional information
   regarding copyright ownership.  The ASF licenses this file
   to you under the Apache License, Version 2.0 (the
   "License"); you may not use this file except in compliance
   with the License.  You may obtain a copy of the License at

..   http://www.apache.org/licenses/LICENSE-2.0

.. Unless required by applicable law or agreed to in writing,
   software distributed under the License is distributed on an
   "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
   KIND, either express or implied.  See the License for the
   specific language governing permissions and limitations
   under the License.


Package ``apache-airflow-providers-huawei``

Release: ``1.7.0``


Huawei Cloud integration (including `Huawei Cloud <https://www.huaweicloud.com/intl/en-us/>`__).


Provider package
----------------

This is a provider package for ``huawei`` provider. All classes for this provider package
are in ``airflow.providers.huawei`` python package.

You can find package information and changelog for the provider
in the `documentation <https://airflow.apache.org/docs/apache-airflow-providers-huawei/1.7.0/>`_.


Installation
------------

You can install this package on top of an existing Airflow 2 installation (see ``Requirements`` below
for the minimum Airflow version supported) via
``pip install apache-airflow-providers-huawei``

The package supports the following python versions: 3.7,3.8,3.9,3.10

Requirements
------------

======================  ==================
PIP package             Version required
======================  ==================
``apache-airflow``      ``>=2.5.0``
``psycopg2``            ``>=2.9.4``
``huaweicloudsdkcore``  ``>=3.1.78``
``esdk-obs-python``     ``>=3.22.2``
``huaweicloudsdkdws``   ``>=3.1.21``
``huaweicloudsdksmn``   ``>=3.1.19``
``huaweicloudsdkdli``   ``==3.1.67``
``huaweicloudsdkcdm``   ``>=3.1.78``
``huaweicloudsdkdlf``   ``>=3.1.19``
``huaweicloudsdkiam``   ``>=3.1.19``
``huaweicloudsdkmrs``   ``>=3.1.58``
======================  ==================

Cross provider package dependencies
-----------------------------------

Those are dependencies that might be needed in order to use all the features of the package.
You need to install the specified provider packages in order to use them.

You can install such cross-provider dependencies when installing from PyPI. For example:

.. code-block:: bash

    pip install apache-airflow-providers-huawei[common.sql]


============================================================================================================  ==============
Dependent package                                                                                             Extra
============================================================================================================  ==============
`apache-airflow-providers-common-sql <https://airflow.apache.org/docs/apache-airflow-providers-common-sql>`_  ``common.sql``
============================================================================================================  ==============

 .. Licensed to the Apache Software Foundation (ASF) under one
    or more contributor license agreements.  See the NOTICE file
    distributed with this work for additional information
    regarding copyright ownership.  The ASF licenses this file
    to you under the Apache License, Version 2.0 (the
    "License"); you may not use this file except in compliance
    with the License.  You may obtain a copy of the License at

 ..   http://www.apache.org/licenses/LICENSE-2.0

 .. Unless required by applicable law or agreed to in writing,
    software distributed under the License is distributed on an
    "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
    KIND, either express or implied.  See the License for the
    specific language governing permissions and limitations
    under the License.


.. NOTE TO CONTRIBUTORS:
   Please, only add notes to the Changelog just below the "Changelog" header when there are some breaking changes
   and you want to add an explanation to the users on how they are supposed to deal with them.
   The changelog is updated and maintained semi-automatically by release manager.

Changelog
---------
1.7.0
.....

Features
~~~~~~~~~
* ``Adjust utils directory structure(!63)``
* ``Add ModerArts Integration(!61)``

1.6.0
.....

Features
~~~~~~~~~
* ``Add Huawei Cloud DWS test cases and example dags and document(!57)``
* ``Fix return type of get_conn of DWSSqlHook(!56)``
* ``Add DWSExecuteQueryOperator and fix DWSSqlHook and DWSClusterSensor(!55)``
* ``Add Huawei Cloud DLI example dags and documents(!54)``
* ``Add test cases for new features in DLI(!53)``
* ``Add new operators, sensors and methods for hooks about DLI(!52)``

1.5.1
.....

Features
~~~~~~~~~
* ``Add template field "variables" for CDMStartJobOperator(!50)``

1.5.0
.....

Features
~~~~~~~~~
* ``Fix docs(!47)``
* ``Add example code for CDMStartJobOperator and supplementary document(!45)``
* ``Add parameter "variables" for CDMStartJobOperator(!44)``

1.4.0
.....

Features
~~~~~~~~~

* ``Add DLIShowElasticResourcePoolStatusSensor (!42)``
* ``Add Huawei Cloud DLI document for new operators (!38)``
* ``Add Huawei Cloud DLI example dags (!37)``
* ``Add test cases for new features in DLI (!36)``
* ``Add new operators, trigger and methods for hooks about DLI (!35)``

1.3.0
.....

Features
~~~~~~~~~

* ``Add deferred mode for MRSCreateClusterOperator (!33)``
* ``Fix stop_job function of MRSHook !(32)``
* ``Add and fix document for MRS and DLI (!30)``
* ``Add test system sample code for MRS (!29)``
* ``Add MRSCreateExecuteJobOperator with deferrable mode and add MRSShowJobResultSensor (!27)``
* ``Add test cases for MRS (!28)``

1.2.0
.....

Features
~~~~~~~~~

* ``Fix docstring (!25)``
* ``Add warning according to the DLI product Bulletin (!25)``
* ``Add deferrable mode to DLISparkCreateBatchJobOperator and DLIRunSqlJobOperator (!25)``
* ``The python sdk version of dli is changed from 3.1.66 to 3.1.67 (!25)``

1.1.0
.....

Features
~~~~~~~~~

* ``Add Huawei Cloud MRS hook,operators, and sensors (!19)``
* ``Add Huawei Cloud MRS test and example dags (!19)``
* ``Add "tags" to template_fields for SMNPublishMessageTemplateOperator (!19)``
* ``Fix the method docstring for create_cluster method of DWSHook (!19)``
* ``Fix example mrs dags (!19)``
* ``Add MRS docs and modify other docs (!19)``
* ``Add MRS dependencies (!19)``

1.0.3
.....

Bug Fixes
~~~~~~~~~

* ``Fix the DLISparkCreateBatchJobOperator parameter (!17)``

1.0.2
.....

Bug Fixes
~~~~~~~~~

* ``Fix the Connections extra param obs-bucket (!15)``

1.0.1
.....

Bug Fixes
~~~~~~~~~

* ``Fix mistakenly added install_requires for provider (!12)``

1.0.0
.....

Initial version of the provider.
