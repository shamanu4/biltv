Ext.ux.menu = {
    'scrambler': [
        {
            'xtype': 'tbseparator'
        },{
            'id': 'menu-scrambler-button',
            'xtype': 'tbbutton',
            'text': 'Скрамблер',
            'menu': [
                {
                    'id': 'menu-scrambler-card-button',
                    'handler': Engine.menu.scrambler.card.openGrid,
                    'text': 'Карточки'                    
                },{
                    'text': 'Стволы'
                }
            ]
        }
    ],
    'cashier': [
        {
            'xtype': 'tbseparator'
        },{
            'id': 'menu-cashier-button',
            'xtype': 'tbbutton',
            'text': 'Касса',
            'menu': [
                {
                    'id': 'menu-cashier-abonent-button',
                    'handler': Engine.menu.cashier.abonent.openGrid,
                    'text': 'Пользователи'
                },{
                    'id': 'menu-cashier-register-button',
                    'handler': Engine.menu.cashier.register.openGrid,
                    'text': 'Реестры',
                    'oid': 0,
                    'my_owner_ct_id':0
                },{
                    'id': 'menu-cashier-payment-button',
                    'handler': Engine.menu.cashier.payment.openForm,
                    'text': 'Оплаты',
					'oid': 0,
					'my_owner_ct_id':0
                },{
                    'id': 'menu-cashier-registers-form-button',
                    'handler': Engine.menu.cashier.register.openForm,
                    'text': 'Отчёт по оплатам',
                    'oid': 0,
                    'my_owner_ct_id':0
                },{
                    'id': 'menu-cashier-report-button',
                    'handler': Engine.menu.cashier.report.launch,
                    'text': 'Отчет по задолженностям',
                    'oid': 0,
                    'my_owner_ct_id':0
                },{
                    'id': 'menu-cashier-illegal-button',
                    'handler': Engine.menu.cashier.illegal.openGrid,
                    'text': 'Отчет по нелегалам',
                    'oid': 0,
                    'my_owner_ct_id':0
                },{
                    'id': 'menu-cashier-statements-button',
                    'handler': Engine.menu.cashier.statements.launch,
                    'text': 'ПриватБанк Выписки',
                    'oid': 0,
                    'my_owner_ct_id':0
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
            'text': 'Адрес',
            'menu': [
                {
                    'id': 'menu-address-city-button',
                    'handler': Engine.menu.address.city.openGrid,
                    'text': 'Города'
                },{
                    'id': 'menu-address-street-button',
                    'handler': Engine.menu.address.street.openGrid,
                    'text': 'Улицы'
                },{
                    'id': 'menu-address-house-button',
                    'handler': Engine.menu.address.house.openGrid,
                    'text': 'Номера домов'
                },{
                    'id': 'menu-address-building-button',
                    'handler': Engine.menu.address.building.openGrid,
                    'text': 'Дома'
                }
            ]
        }
    ]
};

