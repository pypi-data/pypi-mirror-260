#!/usr/bin/python3
""" Glerm, a puzzle game """
# Copyright (C) 2022 Gwyn Ciesla

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import getpass

class TILES: # pylint: disable=too-few-public-methods
    """ The tiles the board is made of """
    horiz = 0
    vert = 0
    image = 0
    rect = 0
    new = 0

def tiles_init(tlist, blank_tile, blank_tile_core):
    """ Create the tiles """
    over = 14
    while over > 0:
        down = 14
        while down > 0:
            newtile = TILES()
            newtile.horiz = over*48-48
            newtile.vert = down*48-48
            if 6 <= over <= 9 and 6 <= down <= 9:
                newtile.image = blank_tile_core
            else:
                newtile.image = blank_tile
            newtile.rect = newtile.image.get_rect()
            tlist.append(newtile)
            down -= 1
        over -= 1

    return tlist

#Game object class, used for the PLAYER.and the chits
class GAMEOBJECT: # pylint: disable=too-few-public-methods
    """ The objects used in the game """
    horiz = 0
    vert = 0
    image = 0
    color = 0
    rect = 0
    new = 0
    dir = 0
    moved = 0

def chit_shift(clist, nchit):
    """ displace any chit in the new chit's location """
    for chit in clist:
        chit.vert = 0
        chit.horiz = 0
        if chit.rect.centerx <= 240 and nchit.rect.centerx <= 240 \
            and chit.rect.centery == nchit.rect.centery:
            chit.horiz = 48
            chit.vert = 0
            chit.rect = chit.rect.move([chit.horiz, chit.vert])
        if chit.rect.centerx >= 432 and nchit.rect.centerx >= 432 \
            and chit.rect.centery == nchit.rect.centery:
            chit.horiz = -48
            chit.vert = 0
            chit.rect = chit.rect.move([chit.horiz, chit.vert])
        if chit.rect.centery <= 240 and nchit.rect.centery <= 240 \
            and chit.rect.centerx == nchit.rect.centerx:
            chit.horiz = 0
            chit.vert = 48
            chit.rect = chit.rect.move([chit.horiz, chit.vert])
        if chit.rect.centery >= 432 and nchit.rect.centery >= 432 \
            and chit.rect.centerx == nchit.rect.centerx:
            chit.horiz = 0
            chit.vert = -48
            chit.rect = chit.rect.move([chit.horiz, chit.vert])

    return clist

def chit_check(clist):
    """ Have any chits made it into the core? """
    brchd = 0
    for check_chit in clist:
        if check_chit.rect.centerx >= 240 and check_chit.rect.centerx <= 432 \
            and check_chit.rect.centery >= 240 and check_chit.rect.centery <= 432:
            return clist, 1

    return clist, brchd

def score_file(scr):
    """ Write high score if warranted """
    scorefilename = os.path.join(os.path.expanduser('~' +  getpass.getuser()), '.glerm_score')
    if not os.path.isfile(scorefilename):
        open(scorefilename, 'a', encoding='utf-8').close() # pylint: disable=consider-using-with
    with open(scorefilename, 'r', encoding='utf-8') as scorefile:
        oldscore = scorefile.readline()
    if not oldscore:
        oldscore = 0
    if scr > int(oldscore):
        with open(scorefilename, 'w', encoding='utf-8') as scorefile:
            scorefile.write(str(scr) + '\n')
        h_score = scr
    else:
        h_score = oldscore

    return h_score
