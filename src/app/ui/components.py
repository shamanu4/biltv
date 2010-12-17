# -*- coding: utf-8 -*-
MenuSection = {
    'scrambler': [
        {
            'xtype': 'tbseparator'
        },{
            'id': 'menu-scrambler-button',
            'xtype': 'tbbutton',
            'text': u'Скрамблер',
            'menu': [
                {
                    'text': u'Каналы'
                },{
                    'text': u'Стволы'
                },
            ]
        }
    ],
    'cashier': [
        {
            'xtype': 'tbseparator'
        },{
            'id': 'menu-cashier-button',
            'xtype': 'tbbutton',
            'text': u'Касса',
            'menu': [
                {
                    'text': u'Item One'
                },{
                    'text': u'Item Two'
                },{
                    'text': u'Item Three'
                }
            ]
        }
    ],
    'address': [
        {
            'xtype': 'tbseparator'
        },{
            'id': 'menu-address-button',
            'xtype': 'tbbutton',
            'text': u'Адрес',
            'menu': [
                {
                    'id': 'menu-address-city-button',
                    'handler': 'Engine.menu.address.city.showGrid',
                    'text': u'Города'
                },{
                    'id': 'menu-address-street-button',
                    'text': u'Улицы'
                },{
                    'id': 'menu-address-house-button',
                    'text': u'Номера домов'
                },{
                    'id': 'menu-address-building-button',
                    'text': u'Дома'
                }
            ]
        }
    ]
}