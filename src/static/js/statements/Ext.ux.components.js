Ext.ux.msg = function () {
    var msgCt;

    function createBox(title, text, type) {
        return ['<div class="msg">',
            '<div class="x-box-tl"><div class="x-box-tr"><div class="x-box-tc"></div></div></div>',
            '<div class="x-box-ml"><div class="x-box-mr"><div class="x-box-mc">',
            '<div class="ext-mb-icon ', type , '">',
            '<h3>', title, '</h3>', text,
            '</div></div></div></div>',
            '<div class="x-box-bl"><div class="x-box-br"><div class="x-box-bc"></div></div></div>',
            '</div>'].join('');
    }

    return function (title, text, type, callback) {
        if (type == "ext-mb-error") {
            var delay = 10;
        } else if (type == "ext-mb-invisible") {
            var delay = 1
        } else {
            var delay = 3
        }
        if (!msgCt) {
            msgCt = Ext.DomHelper.insertFirst(document.body, {id: 'msg-div'}, true)
        }
        msgCt.alignTo(document, 't-t');
        var m = Ext.DomHelper.append(msgCt, {html: createBox(title, text, type)}, true);
        if (Ext.isFunction(callback)) {
            m.slideIn('t').pause(delay).ghost("t", {remove: true, callback: callback});
        } else {
            m.slideIn('t').pause(delay).ghost("t", {remove: true});
        }
    }
}();

Ext.ux.traceback = function () {

    function createBox(text, token) {

        return [
            '<form action="/traceback/" id="traceback-form" method="POST">',
            '<input type="hidden" name="csrfmiddlewaretoken" value="' + token + '" />',
            '<label for="traceback-content">трейсбек:</label>',
            '<br />',
            '<textarea id="traceback-content" cols="75" rows="8" name=traceback disabled>',
            text,
            '</textarea>',
            '<br />',
            '<label for="traceback-description">',
            'опишите Ваши действия перед сбоем <br />',
            'это поможет решить проблему быстрее <br />',
            '</label>',
            '<textarea id="traceback-descripton" cols="75" rows="10" name=traceback-descr>',
            '</textarea>',
            '<br />',
            '</form>',
        ].join('')
    }

    return function (title, text, token) {

        new Ext.Window({
            title: title,
            plain: true,
            html: createBox(text, token),
            modal: true,
            width: 600,
            buttons: [
                {
                    text: 'отослать отчёт',
                    handler: function () {
                        $("#traceback-content").removeAttr("disabled");
                        Ext.get("traceback-form").dom.submit();
                    }
                }
            ],
        }).show();
    }

}();

/*!
 * Ext JS Library 3.4.0
 * Copyright(c) 2006-2011 Sencha Inc.
 * licensing@sencha.com
 * http://www.sencha.com/license
 */
Ext.ns('Ext.ux.grid');

/**
 * @class Ext.ux.grid.BufferView
 * @extends Ext.grid.GridView
 * A custom GridView which renders rows on an as-needed basis.
 */
Ext.ux.grid.BufferView = Ext.extend(Ext.grid.GridView, {
    /**
     * @cfg {Number} rowHeight
     * The height of a row in the grid.
     */
    rowHeight: 19,

    /**
     * @cfg {Number} borderHeight
     * The combined height of border-top and border-bottom of a row.
     */
    borderHeight: 2,

    /**
     * @cfg {Boolean/Number} scrollDelay
     * The number of milliseconds before rendering rows out of the visible
     * viewing area. Defaults to 100. Rows will render immediately with a config
     * of false.
     */
    scrollDelay: 100,

    /**
     * @cfg {Number} cacheSize
     * The number of rows to look forward and backwards from the currently viewable
     * area.  The cache applies only to rows that have been rendered already.
     */
    cacheSize: 20,

    /**
     * @cfg {Number} cleanDelay
     * The number of milliseconds to buffer cleaning of extra rows not in the
     * cache.
     */
    cleanDelay: 500,

    initTemplates: function () {
        Ext.ux.grid.BufferView.superclass.initTemplates.call(this);
        var ts = this.templates;
        // empty div to act as a place holder for a row
        ts.rowHolder = new Ext.Template(
            '<div class="x-grid3-row {alt}" style="{tstyle}"></div>'
        );
        ts.rowHolder.disableFormats = true;
        ts.rowHolder.compile();

        ts.rowBody = new Ext.Template(
            '<table class="x-grid3-row-table" border="0" cellspacing="0" cellpadding="0" style="{tstyle}">',
            '<tbody><tr>{cells}</tr>',
            (this.enableRowBody ? '<tr class="x-grid3-row-body-tr" style="{bodyStyle}"><td colspan="{cols}" class="x-grid3-body-cell" tabIndex="0" hidefocus="on"><div class="x-grid3-row-body">{body}</div></td></tr>' : ''),
            '</tbody></table>'
        );
        ts.rowBody.disableFormats = true;
        ts.rowBody.compile();
    },

    getStyleRowHeight: function () {
        return Ext.isBorderBox ? (this.rowHeight + this.borderHeight) : this.rowHeight;
    },

    getCalculatedRowHeight: function () {
        return this.rowHeight + this.borderHeight;
    },

    getVisibleRowCount: function () {
        var rh = this.getCalculatedRowHeight(),
            visibleHeight = this.scroller.dom.clientHeight;
        return (visibleHeight < 1) ? 0 : Math.ceil(visibleHeight / rh);
    },

    getVisibleRows: function () {
        var count = this.getVisibleRowCount(),
            sc = this.scroller.dom.scrollTop,
            start = (sc === 0 ? 0 : Math.floor(sc / this.getCalculatedRowHeight()) - 1);
        return {
            first: Math.max(start, 0),
            last: Math.min(start + count + 2, this.ds.getCount() - 1)
        };
    },

    doRender: function (cs, rs, ds, startRow, colCount, stripe, onlyBody) {
        var ts = this.templates,
            ct = ts.cell,
            rt = ts.row,
            rb = ts.rowBody,
            last = colCount - 1,
            rh = this.getStyleRowHeight(),
            vr = this.getVisibleRows(),
            tstyle = 'width:' + this.getTotalWidth() + ';height:' + rh + 'px;',
        // buffers
            buf = [],
            cb,
            c,
            p = {},
            rp = {tstyle: tstyle},
            r;
        for (var j = 0, len = rs.length; j < len; j++) {
            r = rs[j];
            cb = [];
            var rowIndex = (j + startRow),
                visible = rowIndex >= vr.first && rowIndex <= vr.last;
            if (visible) {
                for (var i = 0; i < colCount; i++) {
                    c = cs[i];
                    p.id = c.id;
                    p.css = i === 0 ? 'x-grid3-cell-first ' : (i == last ? 'x-grid3-cell-last ' : '');
                    p.attr = p.cellAttr = "";
                    p.value = c.renderer(r.data[c.name], p, r, rowIndex, i, ds);
                    p.style = c.style;
                    if (p.value === undefined || p.value === "") {
                        p.value = "&#160;";
                    }
                    if (r.dirty && typeof r.modified[c.name] !== 'undefined') {
                        p.css += ' x-grid3-dirty-cell';
                    }
                    cb[cb.length] = ct.apply(p);
                }
            }
            var alt = [];
            if (stripe && ((rowIndex + 1) % 2 === 0)) {
                alt[0] = "x-grid3-row-alt";
            }
            if (r.dirty) {
                alt[1] = " x-grid3-dirty-row";
            }
            rp.cols = colCount;
            if (this.getRowClass) {
                alt[2] = this.getRowClass(r, rowIndex, rp, ds);
            }
            rp.alt = alt.join(" ");
            rp.cells = cb.join("");
            buf[buf.length] = !visible ? ts.rowHolder.apply(rp) : (onlyBody ? rb.apply(rp) : rt.apply(rp));
        }
        return buf.join("");
    },

    isRowRendered: function (index) {
        var row = this.getRow(index);
        return row && row.childNodes.length > 0;
    },

    syncScroll: function () {
        Ext.ux.grid.BufferView.superclass.syncScroll.apply(this, arguments);
        this.update();
    },

    // a (optionally) buffered method to update contents of gridview
    update: function () {
        if (this.scrollDelay) {
            if (!this.renderTask) {
                this.renderTask = new Ext.util.DelayedTask(this.doUpdate, this);
            }
            this.renderTask.delay(this.scrollDelay);
        } else {
            this.doUpdate();
        }
    },

    onRemove: function (ds, record, index, isUpdate) {
        Ext.ux.grid.BufferView.superclass.onRemove.apply(this, arguments);
        if (isUpdate !== true) {
            this.update();
        }
    },

    doUpdate: function () {
        if (this.getVisibleRowCount() > 0) {
            var g = this.grid,
                cm = g.colModel,
                ds = g.store,
                cs = this.getColumnData(),
                vr = this.getVisibleRows(),
                row;
            for (var i = vr.first; i <= vr.last; i++) {
                // if row is NOT rendered and is visible, render it
                if (!this.isRowRendered(i) && (row = this.getRow(i))) {
                    var html = this.doRender(cs, [ds.getAt(i)], ds, i, cm.getColumnCount(), g.stripeRows, true);
                    row.innerHTML = html;
                }
            }
            this.clean();
        }
    },

    // a buffered method to clean rows
    clean: function () {
        if (!this.cleanTask) {
            this.cleanTask = new Ext.util.DelayedTask(this.doClean, this);
        }
        this.cleanTask.delay(this.cleanDelay);
    },

    doClean: function () {
        if (this.getVisibleRowCount() > 0) {
            var vr = this.getVisibleRows();
            vr.first -= this.cacheSize;
            vr.last += this.cacheSize;

            var i = 0, rows = this.getRows();
            // if first is less than 0, all rows have been rendered
            // so lets clean the end...
            if (vr.first <= 0) {
                i = vr.last + 1;
            }
            for (var len = this.ds.getCount(); i < len; i++) {
                // if current row is outside of first and last and
                // has content, update the innerHTML to nothing
                if ((i < vr.first || i > vr.last) && rows[i].innerHTML) {
                    rows[i].innerHTML = '';
                }
            }
        }
    },

    removeTask: function (name) {
        var task = this[name];
        if (task && task.cancel) {
            task.cancel();
            this[name] = null;
        }
    },

    destroy: function () {
        this.removeTask('cleanTask');
        this.removeTask('renderTask');
        Ext.ux.grid.BufferView.superclass.destroy.call(this);
    },

    layout: function () {
        Ext.ux.grid.BufferView.superclass.layout.call(this);
        this.update();
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
        options = options || {}
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
                    this.store.save()
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
                    this.searchfield.setValue('')
                    this.store.baseParams.filter_value = ''
                    this.store.load()
                },
                scope: this
            },
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
                this.store.baseParams.filter_value = this.searchfield.getValue()
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
        }
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.apply(this, options);
        Ext.ux.CustomGrid.superclass.initComponent.apply(this, arguments);
    }
});


var entry_ds_model = Ext.data.Record.create([
    'id',
    'timestamp',
    'amount',
]);


Ext.ux.Entry_store_config = {
    api: {
        read: EntryGrid.read,
        create: EntryGrid.foo,
        update: EntryGrid.update,
        destroy: EntryGrid.foo
    },
    restful: true,
    autoLoad: true,
    autoSave: false,
    storeId: 'entry-store',
    reader: new Ext.data.JsonReader({
        root: 'data',
        totalProperty: 'total',
        //idProperty: 'id',
        fields: [
            'id',
            'timestamp',
            'amount',
        ]
    }),
    writer: new Ext.data.JsonWriter({
        encode: false,
        writeAllFields: true,
        listful: true
    }),
    listeners:{
        write: function (store,action,result,res,rs) {
            if(store.client && store.client.onWrite) {
                store.client.onWrite(res.result)
            }
        }
    }
};

Ext.ux.EntryStore = Ext.extend(Ext.data.DirectStore, {
    initComponent: function(options) {
        config: Ext.ux.Entry_store_config;
        options = options || {};
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.apply(this, options);
        Ext.ux.EntryStore.superclass.initComponent.apply(this, arguments);
    }
});


Ext.ux.EntryGrid = Ext.extend(Ext.ux.CustomGrid, {
    ds_model: entry_ds_model,
    title: 'Entry',
    columns: [
        {header: "Id", dataIndex: 'id'},
        {header: "Amount", dataIndex: 'amount', editor: new Ext.form.TextField()},
        {header: "Timestamp", dataIndex: 'timestamp', editor: new Ext.form.TextField()},
    ],
    initComponent: function(options) {
        options = options || {};
        var config = {};
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.apply(this, options);
        Ext.ux.EntryGrid.superclass.initComponent.apply(this, arguments);
    }
});

Ext.reg('ext:ux:entry-grid', Ext.ux.EntryGrid);