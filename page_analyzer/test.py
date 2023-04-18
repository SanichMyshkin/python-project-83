from dotenv import load_dotenv
from flask import Flask, render_template, \
    flash, request, redirect, url_for
import os

from datetime import datetime
from page_analyzer.connected import get_all_db, \
    insert_to_db, connect_to_db, get_id
from page_analyzer.checks_request import get_data_html, get_status
from page_analyzer.validate import is_valid, get_normalize_domain

connection = connect_to_db()

current_url = "https://www.hexlet.io"
id = get_id(connection, current_url)

print(id)