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
                        text: 'Отправить',
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
                }), {
                    region: 'west',
                    id: 'west-panel', // see Ext.getCmp() below
                    title: 'West',
                    split: true,
                    width: 1000,
                    minSize: 100,
                    collapsible: true,
                    margins: '0 0 0 5'
                },
                // in this instance the TabPanel is not wrapped by another panel
                // since no title is needed, this Panel is added directly
                // as a Container
                new Ext.TabPanel({
                    region: 'center', // a center region is ALWAYS required for border layout
                    deferredRender: false,
                    activeTab: 0,     // first tab initially active
                    collapsible: true,
                    split: true,
                    width: 1000,
                    minSize: 100,
                    maxSize: 1200,
                    items: []
                })
            ]
        };
        // get a reference to the HTML element with id "hideit" and add a click listener to it
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.MainViewport.superclass.initComponent.apply(this, arguments);
    }
});