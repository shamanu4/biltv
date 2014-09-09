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
            }, Ext.ux.Entry_store_config))
        });
        panel.add(tab);
        return true;
    };

    MainApi.get_categories(window.day, function (response) {
        var panel = Ext.getCmp("center-tab-panel");
        Ext.each(response.data, function (category) {
            window.panelAddTab(panel, category.name, category.id, category.svc_type);
        })
    });

});


