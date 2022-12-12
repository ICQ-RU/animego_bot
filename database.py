"""
This file is a part of AnimeGo Monitoring Bot.

AnimeGo Monitoring Bot is a Telegram bot supposed to check the release of new episodes at <https://animego.org/>
Copyright (C) 2021 Nerovik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

import sqlite3

class Database:

    def __init__(self, db_file):
        self.conn = sqlite3.connect(db_file, check_same_thread=False)
        self.cursor = self.conn.cursor()

    def userExists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `userId` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def getId(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `userId` = ?", (user_id,))
        return result.fetchone()[0]

    def addUser(self, user_id):
        self.cursor.execute("INSERT INTO `users` (`userId`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def setTracking(self, id, title_link):
        self.cursor.execute("UPDATE `users` SET `tracking` = ? WHERE `id` = ?", (title_link, id))
        return self.conn.commit()

    def getTracking(self, id):
        result = self.cursor.execute("SELECT `tracking` FROM `users` WHERE `id` = ?", (id,))
        return result.fetchone()[0]

    def getIds(self):
        result = self.cursor.execute("SELECT `id` FROM `users`")
        return result.fetchall()

    def getUserId(self, id):
        result = self.cursor.execute("SELECT `userId` FROM `users` WHERE `id` = ?", (id,))
        return result.fetchone()

    def setEpisodes(self, id, episodes):
        self.cursor.execute("UPDATE `users` SET `episodes` = ? WHERE `id` = ?", (episodes, id))
        return self.conn.commit()

    def getEpisodes(self, id):
        result = self.cursor.execute("SELECT `episodes` FROM `users` WHERE `id` = ?", (id,))
        return result.fetchone()[0]

    def close(self):
        self.conn.close()