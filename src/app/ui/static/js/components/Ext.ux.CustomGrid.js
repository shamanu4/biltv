Ext.ux.CustomGridNE = Ext.extend(Ext.grid.EditorGridPanel,{
    store: null,
    ds_model: null,
	closable: true,
    columns: [],
    height: 500,
    boxMaxWidth: 1000,
    instance: null,
    viewConfig: {
        //forceFit:true
    },
    onRender:function() {
        Ext.ux.CustomGrid.superclass.onRender.apply(this, arguments);
        this.store.client=this;
        this.store.load();
    },
    addAction: function() {
        // overrides in instance
    },
    searchAction: function() {
        this.store.baseParams.filter_value = this.searchfield.getValue();
		this.store.load()
	},
    initComponent: function(){
        var config = {
            frame:true,
            tbar: [
            {
                text: 'Add',
                icon: '/static/extjs/custom/plus_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.addAction()
                },
                scope: this
            },
            new Ext.Toolbar.Spacer(),
            this.searchfield = new Ext.form.TextField({
                listeners: {
                    specialkey: {
                        fn: function(field, e){                            
                            if (e.getKey() == e.ENTER) {                                
                                this.searchAction()
                            }
                        },
                        scope: this
                    }
                }
            }),
            new Ext.Toolbar.Spacer(),
            {
                icon: '/static/extjs/custom/search_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.searchAction()
                },
                scope: this
            },{
                icon: '/static/extjs/custom/delete_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    var $this = this;
                    $this.searchfield.setValue('');
                    $this.store.baseParams.filter_value = '';
                    $this.store.load()
                },
                scope: this
            }
            ],
            bbar: new Ext.PagingToolbar({
                pageSize: this.pageSize || 16,
                store: this.store
            }),
            listeners: {
                    beforeclose: {
                        fn: function(obj) {
                            obj.hide()
                        }
                    },
                    beforedestroy: {
                        fn: function(e) {
                            return false;
                        }
                    }
            }
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.CustomGrid.superclass.initComponent.apply(this, arguments);
    }
});

Ext.ux.CustomGrid = Ext.extend(Ext.grid.EditorGridPanel,{
    store: null,
    ds_model: null,
    columns: [],
    height: 500,
    boxMaxWidth: 1000,
    instance: null,
    viewConfig: {
        //forceFit:true
    },
    onRender:function() {
        Ext.ux.CustomGrid.superclass.onRender.apply(this, arguments);
        this.store.client=this;
        this.store.load();
    },
    onWrite: function(result) {
        if(result.success) {
            //this.store.commitChanges();
        } else {
            this.selModel.selectRow(this.unsaved_row)
        }
    },
    initComponent: function(options) {
        options = options || {};
        var config = {
            frame:true,
            closable: true,
            current_row: 0,
            unsaved_row: 0,            
            tbar: [{
                text: 'Apply',
                icon: '/static/extjs/custom/tick_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {		    
                    this.store.save();
                    //this.store.commitChanges();
                },
                scope: this
            },{
                text: 'Add',
                icon: '/static/extjs/custom/plus_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.store.insert(
                        0,
                        new this.ds_model()
                    );
                    this.startEditing(0,1);
                },
                scope: this
            },{
                text: 'Cancel',
                icon: '/static/extjs/custom/block_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.store.reload()
                },
                scope: this
            },
            new Ext.Toolbar.Spacer(),
             this.searchfield = new Ext.form.TextField({
                listeners: {
                    specialkey: {
                        fn: function(field, e){
                            if (e.getKey() == e.ENTER) {
                                this.searchAction()
                            }
                        },
                        scope: this
                    }                
                }
            }),
            new Ext.Toolbar.Spacer(),
            {
                icon: '/static/extjs/custom/search_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.searchAction()
                },
                scope: this
            },{
                icon: '/static/extjs/custom/delete_16.png',
                cls: 'x-btn-text-icon',
                handler: function() {
                    this.searchfield.setValue('');
                    this.store.baseParams.filter_value = '';
                    this.store.load()
                },
                scope: this
            }
            ],
            bbar: new Ext.PagingToolbar({
                pageSize:  this.pageSize || 16,
                store: this.store
            }),
            listeners: {
                    beforeclose: {
                        fn: function(obj) {
                            obj.hide()
                        }
                    },
                    beforedestroy: {
                        fn: function(e) {
                            return false;
                        }
                    }
            },
            searchAction: function() {
                this.store.baseParams.filter_value = this.searchfield.getValue();
                this.store.load()
            }
          /*  sm: new Ext.grid.RowSelectionModel({
                singleSelect: true,
                listeners: {
                    rowselect: {
                        fn: function(sm,index,record) {
                            //if(this.current_row != index) {
                            //    this.unsaved_row = this.current_row
                            //    this.current_row = index
                            //    this.store.save()
                            //    this.store.commitChanges();
                            //}
                        },
                        scope: this
                    }
                }
            })
          */
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.apply(this, options);
        Ext.ux.CustomGrid.superclass.initComponent.apply(this, arguments);
    }
});

