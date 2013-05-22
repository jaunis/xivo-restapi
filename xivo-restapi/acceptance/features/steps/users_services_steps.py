# -*- coding: UTF-8 -*-

# Copyright (C) 2012  Avencall
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA..

from acceptance.features.steps.helpers.rest_users import RestUsers
from lettuce.decorators import step
from lettuce.registry import world

rest_users = RestUsers()


@step(u'Then I can enable DND for this user')
def then_i_can_enable_dnd_for_this_user(step):
    result = rest_users.enablednd(world.userid)
    assert result.status == 200, "unable to set dnd on user %d got result %d instead of 200" % (world.userid, result.status)


@step(u'Then I can disable DND for this user')
def then_i_can_disable_dnd_for_this_user(step):
    result = rest_users.disablednd(world.userid)
    assert result.status == 200, "unable to disable dnd on user %d got result %d instead of 200" % (world.userid, result.status)
