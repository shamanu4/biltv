Ext.onReady(function () {

    Ext.state.Manager.setProvider(new Ext.state.CookieProvider({
        expires: new Date(new Date().getTime() + (1000 * 60 * 60 * 24 * 30)) // 30 days
    }));

    var vp = new Ext.ux.MainViewport();
    Ext.ux.msg('Грузимся ....', 'пожалуйста подождите', "ext-mb-invisible");

    Engine = window.Engine || {};
    Engine.vp = vp;
    Engine.auth.checkAuth();

    $.alerts._overlay = function (status) {
        switch (status) {
            case 'show':
                alertsMask.show();
                break;
            case 'hide':
                alertsMask.hide();
                break;
        }
    };

    window.panelAddStatement = function(panel, statement_id) {
        var panel_id = "main-grid";
        var e = Ext.getCmp(panel_id);
        if(e) {
            return false;
        }
        var tab = new Ext.ux.EntryGrid({
            title: "виписка "+window.day,
            statement_id: statement_id,
            id: panel_id,
            store: new Ext.ux.EntryStore(Ext.apply({
                baseParams: {
                    start:0,
                    limit:20,
                    filter_fields:[
                        'id',
                        'pid',
                        'amount',
                        'currency',
                        'egrpou',
                        'verbose_name',
                        'account_num',
                        'mfo',
                        'descr',
                        'processed'
                    ],
                    filter_value:'',
                    filter: {'statement__id': window.statement_id, 'category__isnull':true }
                }
            }, Ext.ux.Entry_store_config)),
            update_stats: function() {
                var tab = Ext.getCmp(this.id);
                MainApi.update_stats(0, tab.statement_id, function(response) {
                    tab.lb_total.setValue(response.total);
                    tab.lb_unregistered.setValue(response.unregistered);
                    tab.lb_unprocessed.setValue(response.unprocessed);
                });
            }
        });
        tab.disableDragDrop = false;
        panel.add(tab);
        return tab;
    };

    window.panelAddStatementCat = function(panel, statement_id) {
        var panel_id = "cat-panel-total";
        var e = Ext.getCmp(panel_id);
        if(e) {
            return false;
        }
        var tab = new Ext.ux.EntryGrid({
            title: "Всього "+window.day,
            statement_id: statement_id,
            id: panel_id,
            store: new Ext.ux.EntryStore(Ext.apply({
                baseParams: {
                    start:0,
                    limit:20,
                    filter_fields:[
                        'id',
                        'pid',
                        'amount',
                        'currency',
                        'egrpou',
                        'verbose_name',
                        'account_num',
                        'mfo',
                        'descr',
                        'processed'
                    ],
                    filter_value:'',
                    filter: {'statement__id': window.statement_id, 'category__isnull':false }
                }
            }, Ext.ux.Entry_store_config)),
            update_stats: function() {
                var tab = Ext.getCmp(this.id);
                MainApi.update_stats(0, tab.statement_id, function(response) {
                    tab.lb_total.setValue(response.total_cat);
                    tab.lb_unregistered.setValue(response.unregistered_cat);
                    tab.lb_unprocessed.setValue(response.unprocessed_cat);
                });
            }
        });
        tab.disableDragDrop = true;
        panel.add(tab);
        return tab;
    };

    window.panelAddTab = function(panel, title, category_id, svc_type) {
        svc_type = svc_type || 'UNDEF';
        var panel_id = 'cat-panel-'+category_id;
        var e = Ext.getCmp(panel_id);
        if(e) {
            return false;
        }
        var tab = new Ext.ux.EntryGrid({
            title: title,
            id: panel_id,
            iconCls: 'icon-tab-title-'+svc_type,
            store: new Ext.ux.EntryStore(Ext.apply({
                baseParams: {
                    start: 0,
                    limit: 16,
                    filter_fields: [
                        'id',
                        'pid',
                        'amount',
                        'currency',
                        'egrpou',
                        'verbose_name',
                        'account_num',
                        'mfo',
                        'descr',
                        'processed'
                    ],
                    filter_value: '',
                    filter: {'statement__id': window.statement_id, 'category__pk': category_id }
                }
            }, Ext.ux.Entry_store_config)),
            listeners: {
                activate: function() {
                    if(this.can_create_register) {
                        Ext.getCmp('create-register-btn').enable();
                    } else {
                        Ext.getCmp('create-register-btn').disable();
                    }
                }

            },
            update_stats: function() {
                var tab = Ext.getCmp(this.id);
                MainApi.update_stats(tab.category_id, 0, function(response) {
                    tab.can_create_register = response.can_create_register;
                    if(tab.can_create_register) {
                        Ext.getCmp('create-register-btn').enable();
                    } else {
                        Ext.getCmp('create-register-btn').disable();
                    }
                    tab.lb_total.setValue(response.total);
                    tab.lb_unregistered.setValue(response.unregistered);
                    tab.lb_unprocessed.setValue(response.unprocessed);
                });
            }
        });
        tab.disableDragDrop = false;
        panel.add(tab);
        return tab;
    };

    var panel = Ext.getCmp("west-panel");
    var tab = window.panelAddStatement(panel, window.statement_id)
    tab.update_stats();

    panel = Ext.getCmp("center-tab-panel");
    tab = window.panelAddStatementCat(panel, window.statement_id)
    tab.update_stats();

    MainApi.get_categories(window.day, function (response) {
        var panel = Ext.getCmp("center-tab-panel");
        Ext.each(response.data, function (category) {
            var tab = window.panelAddTab(panel, category.name, category.id, category.svc_type);
            tab.can_create_register = category.can_create_register;
            tab.source_id = category.source_id;
            tab.category_id = category.id;
            tab.update_stats();
        })
    });

});


