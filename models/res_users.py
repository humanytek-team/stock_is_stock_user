# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Manuel Márquez <manuel@humanytek.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import api, fields, models


class ResuUsers(models.Model):
    _inherit = 'res.users'

    is_stock_user = fields.Boolean(
        string='Is a stock user?',
        compute='_compute_is_user_stock',
        search='_search_is_stock_user')

    @api.depends('groups_id')
    def _compute_is_user_stock(self):
        """ Computes value of field is_stock_user """

        group_stock_user = self.env.ref('stock.group_stock_user')
        for user in self:
            user.is_stock_user = False
            if group_stock_user.id in user.groups_id.mapped('id'):
                user.is_stock_user = True

    def _search_is_stock_user(self, operator, value):
        """ Computes the search operation in field is_stock_user"""

        group_stock_user = self.env.ref('stock.group_stock_user')
        stock_users = self.search([('groups_id', 'in', group_stock_user.id)])
        return [('id', 'in', stock_users.mapped('id'))]
