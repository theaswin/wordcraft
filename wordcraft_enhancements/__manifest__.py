# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (c) 2024 ZestyBeanz Technologies.
#    (http://wwww.zbeanztech.com)
#    contact@zbeanztech.com
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

{
    'name': 'WordCraft Customisation',
    'version': '19.0.0.6',
    'summary': 'This module ensures that accounting entries can only be posted if the corresponding Chart of Accounts is approved.',
    'category':'Accounting',
    'website': 'https://dxb.wordcraftgroup.com/',
    'description': """
            Enhancement Of Wordcraft.
    """,
    'author': 'WordCraft',
    'maintainer': 'WordCraft',
    'support': 'WordCraft',
    'license': 'LGPL-3',
    'depends': ['account','contacts'],
    'data': [
        'views/res_partner_view.xml',
        ],
    'test': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': False,
}




