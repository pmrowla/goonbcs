# Copyright (c) 2013 Peter Rowlands

from __future__ import absolute_import

from flask.ext.security import UserMixin, RoleMixin

from . import db


class Conference(db.Model):
    """A college football conference"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    subdivision_id = db.Column(db.Integer, db.ForeignKey('subdivision.id'))
    teams = db.relationship('Team', backref='conference', lazy='dynamic')
    divisions = db.relationship('Division', backref='conference',
                                lazy='dynamic')


class Division(db.Model):
    """A conference division (i.e. the SEC East)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), unique=True)
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'))
    teams = db.relationship('Team', backref='division', lazy='dynamic')


class Poll(db.Model):
    """A single user's poll for a single week"""
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    week_id = db.Column(db.Integer, db.ForeignKey('week.id'))
    moon_poll = db.Column(db.Boolean, default=False)
    votes = db.relationship('Vote', backref='poll', lazy='dynamic')


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, unique=True)
    weeks = db.relationship('Week', backref='season', lazy='dynamic')


class Subdivision(db.Model):
    """A college football subdivision (i.e. FBS)"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    conferences = db.relationship('Conference', backref='subdivision',
                                  lazy='dynamic')


class Team(db.Model):
    """A college football team"""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    school = db.Column(db.String(255), unique=True)
    conference_id = db.Column(db.Integer, db.ForeignKey('conference.id'))
    division_id = db.Column(db.Integer, db.ForeignKey('division.id'))


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    poll_id = db.Column(db.Integer, db.ForeignKey('poll.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    rank = db.Column(db.Integer)
    db.UniqueConstraint('poll_id', 'team_id', name='uidx_poll_team')


class Week(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'))


#######################
# Flask-security models
#######################


roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    confirmed_at = db.Column(db.DateTime())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))
    polls = db.relationship('Poll', backref='user', lazy='dynamic')
