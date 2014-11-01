Ext.ux.MainViewport = Ext.extend(Ext.Viewport, {
    renderTo: Ext.getBody(),

    initComponent: function(){
        var config = {
            layout: 'border',
            items: [
                // create instance immediately
                fp = new Ext.FormPanel({
                    region: 'north',
                    fileUpload: true,
                    height: 60,
                    frame: true,
                    title: 'File Upload Form',
                    labelWidth: 50,
                    layout: 'column',
                    defaults: {
                        allowBlank: false
                    },
                    items: [{
                        xtype: 'datefield',
                        format: 'Y-m-d',
                        fieldLabel: 'Date',
                        name: 'day',
                        id: "form-date-input"
                    },{
                        xtype: 'fileuploadfield',
                        id: 'form-file',
                        emptyText: 'Выберите xls отчет',
                        fieldLabel: 'xls',
                        name: 'xls',
                        buttonText: 'XLS',
                        buttonCfg: {
                            iconCls: 'upload-icon'
                        }
                    },{
                        xtype: 'button',
                        text: 'Відправити',
                        handler: function(){
                            if(fp.getForm().isValid()){
                                fp.getForm().submit({
                                    url: '/statements/upload/',
                                    waitMsg: 'Обработка XLS файла...',
                                    success: function(res, o){
                                        var datestr = fp.getForm().items.items[0].value;
                                        Ext.ux.msg('Загружено', datestr+'.xls saved', Ext.Msg.INFO);
                                        setTimeout(function(){
                                            document.location.href="/statements/"+datestr;
                                        }, 1000)
                                    },
                                    failure: function(res, o) {
                                        ps = JSON.parse(o.response.responseText);
                                        Ext.ux.msg("Error", ps.errors, Ext.Msg.ERROR);
                                    }
                                });
                            }
                        }
                    },{
                        xtype: 'button',
                        text: 'Перейти',
                        handler: function(){
                            if(fp.getForm().items.items[0].value){
                                document.location.href="/statements/"+fp.getForm().items.items[0].value;
                            }
                        }
                    }]
                }),

                new Ext.Panel({
                    region: 'south'
                }),
                new Ext.ux.TabPanel({
                    region: 'west',
                    id: 'west-panel', // see Ext.getCmp() below
//                    title: 'West',
                    split: true,
                    width: 1000,
                    minSize: 100,
                    collapsible: true,
                    margins: '0 0 0 5',
                    tbar: {
                        items:[{
                            xtype: 'button',
                            ui: 'round',
                            text: '_',
                            dock: 'left',
                            handler: function(){
//                                alert('Botton1 Working Now');
                            }
                        }]
                    },
                    items: []
                }),
                // in this instance the TabPanel is not wrapped by another panel
                // since no title is needed, this Panel is added directly
                // as a Container
                new Ext.ux.TabPanel({
                    region: 'center', // a center region is ALWAYS required for border layout
                    id: "center-tab-panel",
                    deferredRender: false,
                    activeTab: 0,     // first tab initially active
                    collapsible: true,
                    split: true,
                    width: 1000,
                    minSize: 100,
                    maxSize: 1200,
                    items: [ ],
                    tbar: {
                        items:[
                            new Ext.ux.NewCategorySelect({
                                id: 'add-new-cat-select',
                                store: new Ext.ux.NewCategoryStore(Ext.apply({
                                    baseParams: {
                                        day: window.day
                                    }
                                }, Ext.ux.Category_store_config))
                            }),
                        {
                            xtype: 'button',
                            ui: 'round',
                            icon: '/static/extjs/custom/plus_16.png',
                            text: 'Додати банк',
                            dock: 'left',
                            handler: function(){
                                var select = Ext.getCmp('add-new-cat-select');
                                var record = select.store.data.items[select.selectedIndex].data;
                                var panel = Ext.getCmp("center-tab-panel");
                                if(select.value) {
                                    var tab = window.panelAddTab(panel, record.name, record.id, record.svc_type);
                                    tab.category_id = record.id;
                                    tab.source_id = record.source_id;
                                }
                            }
                        },{
                            xtype: 'tbseparator'
                        },{
                            xtype: 'button',
                            id: 'create-register-btn',
                            disabled: true,
                            ui: 'round',
                            icon: '/static/extjs/custom/label_16.png',
                            text: 'Створити реєстр',
                            dock: 'left',
                            handler: function(){
                                var tab = Ext.getCmp('center-tab-panel').getActiveTab();
                                MainApi.create_register(tab.category_id, function(response){
                                    tab.update_stats()
                                });
                            }
                        }]
                    }
                })
            ]
        };
        // get a reference to the HTML element with id "hideit" and add a click listener to it
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.MainViewport.superclass.initComponent.apply(this, arguments);
    }
});