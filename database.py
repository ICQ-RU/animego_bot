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

    def user_exists(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return bool(len(result.fetchall()))

    def getId(self, user_id):
        result = self.cursor.execute("SELECT `id` FROM `users` WHERE `user_id` = ?", (user_id,))
        return result.fetchone()[0]

    def add_user(self, user_id):
        self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))
        return self.conn.commit()

    def set_title(self, user_id, title_link):
        self.cursor.execute("UPDATE `users` SET `monitors` = ? WHERE `id` = ?", (title_link, user_id))
        return self.conn.commit()

    def get_title(self, user_id):
        result = self.cursor.execute("SELECT `monitors` FROM `users` WHERE `id` = ?", (user_id,))
        return result.fetchone()[0]

    def get_ids(self):
        result = self.cursor.execute("SELECT `id` FROM `users`")
        return result.fetchall()

    def getUserId(self, id):
        result = self.cursor.execute("SELECT `user_id` FROM `users` WHERE `id` = ?", (id,))
        return result.fetchone()

    def set_episodes(self, user_id, episodes):
        self.cursor.execute("UPDATE `users` SET `episodes` = ? WHERE `id` = ?", (episodes, user_id))
        return self.conn.commit()

    def get_episodes(self, user_id):
        result = self.cursor.execute("SELECT `episodes` FROM `users` WHERE `id` = ?", (user_id,))
        return result.fetchone()[0]

    def close(self):
        self.conn.close()