import datetime as dt
import ipaddress
import json
from collections import defaultdict

import pandas as pd
from flask import Flask, jsonify, request
from intervaltree import IntervalTree

from balanced_binary_search_tree import BST, Node, UserStatus, Record, USER_STATUS_DICT


class UserStatusSearch:
    RECORDS = [
        {'user_id': 1, 'created_at': '2017-01-01T10:00:00', 'status': 'paying'},
        {'user_id': 1, 'created_at': '2017-03-01T19:00:00', 'status': 'paying'},
        {'user_id': 1, 'created_at': '2017-02-01T12:00:00', 'status': 'cancelled'},
        {'user_id': 3, 'created_at': '2017-10-01T10:00:00', 'status': 'paying'},
        {'user_id': 3, 'created_at': '2016-02-01T05:00:00', 'status': 'cancelled'},
    ]

    USER_RECORDS = defaultdict(list)
    USER_RECORDS_BST = defaultdict(Node)
    bst = BST()

    def __init__(self):
        for record in self.RECORDS:
            user_records = self.USER_RECORDS[record['user_id']]
            user_records.append(Record(status=USER_STATUS_DICT[record["status"]],
                                       created_at=dt.datetime.strptime(record["created_at"], '%Y-%m-%dT%H:%M:%S')))
            self.USER_RECORDS[record['user_id']] = user_records

        for k, v in self.USER_RECORDS.items():
            self.USER_RECORDS_BST[k] = self.bst.array_to_bst(sorted(v, key=lambda d: d.created_at))

    def get_status(self, user_id: int, date: dt.datetime):
        if user_id not in self.USER_RECORDS_BST:
            return UserStatus.NOT_PAYING.name
        return self.bst.get_nearest_status(self.USER_RECORDS_BST[user_id], date).data.status.name


class IpRangeSearch:
    RANGES = {
        'london': [
            {'start': '10.10.0.0', 'end': '10.10.255.255'},
            {'start': '192.168.1.0', 'end': '192.168.1.255'},
        ],
        'munich': [
            {'start': '10.12.0.0', 'end': '10.12.255.255'},
            {'start': '172.16.10.0', 'end': '172.16.11.255'},
            {'start': '192.168.2.0', 'end': '192.168.2.255'},
        ]
    }

    interval_tree = IntervalTree()

    def __init__(self):
        for city, ranges in self.RANGES.items():
            for r in ranges:
                self.interval_tree.addi(ipaddress.ip_address(r['start']), ipaddress.ip_address(r['end']), city)

    def get_city(self, ip):
        interval = self.interval_tree.at(ipaddress.ip_address(ip))
        return interval.pop().data if len(interval) else 'NA'


app = Flask(__name__)
user_status_search = UserStatusSearch()
ip_range_search = IpRangeSearch()


@app.route('/user_status/<user_id>')
def user_status(user_id):
    """
    Return user status for a given date

    /user_status/1?date=2017-10-10T10:00:00
    """

    try:
        date = dt.datetime.strptime(str(request.args.get('date')), '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        return jsonify({'error': 'Invalid date format'})

    return jsonify({'user_status': user_status_search.get_status(int(user_id), date)})


@app.route('/ip_city/<ip>')
def ip_city(ip):
    """
    Return city for a given ip

    /ip_city/10.0.0.0
    """
    return jsonify({'city': ip_range_search.get_city(ip)})


@app.route('/transactions')
def aggregate():
    """
    aggregate containing the sum of product_price grouped by user_status and city.
    """
    transactions = []
    with open('./transactions.json') as f:
        for line in f:
            transactions.append(json.loads(line))
        for t in transactions:
            t['city'] = ip_city(t['ip']).json["city"]
            t['user_status'] = user_status_search.get_status(int(t['user_id']), dt.datetime.strptime(t["created_at"], '%Y-%m-%dT%H:%M:%S'))

    df = pd.DataFrame.from_records(transactions)
    return df.groupby(['city', 'user_status'])['product_price'].agg('sum').reset_index().to_json(orient='records')


if __name__ == '__main__':
    app.run(debug=True)
