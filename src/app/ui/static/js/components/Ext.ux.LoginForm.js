Ext.ux.LoginForm = Ext.extend(Ext.form.FormPanel,{
    frame:
        true,
    // configs for FormPanel
    width: 300,
    height: 160,
    padding: 10,
    initComponent: function(){
        var config = {
            buttons:[{
                text: 'ОК',
                handler: function(){
                    this.submitaction()
                },
                scope: this
            }],

            submitaction: function() {
                this.getForm().submit({
                    failure: function(form){
                        var $this = this;
                        if($this.getForm().isValid()) {
                            // Ext.ux.msg('Ошибка авторизации', action.result.msg, Ext.Msg.ERROR);
                        } else {
                            Ext.ux.msg('Ошибка ввода', 'обязательные поля не заполнены', Ext.Msg.ERROR);
                        }
                        $this.ownerCt.loginFailed();
                        $this.getForm().reset()
                    },
                    success: function(form, action){
                        // Ext.ux.msg('Авторизация успешная', action.result.msg, Ext.Msg.INFO);
                        var $this = this;
                        $this.ownerCt.loginSuccess();
                        $this.ownerCt.close()
                    },
                    scope: this
                });
            },

            keys: [
                {
                    key: [Ext.EventObject.ENTER], handler: function() {                      
                        this.submitaction()
                    },
                    scope: this
                }
            ],

            defaults: {anchor: '100%'},
            defaultType: 'textfield',
            items: [{
                fieldLabel: 'Логин',
                allowBlank: false,
                name: 'username'
            },{
                fieldLabel: 'Пароль',
                allowBlank: false,
                name: 'password',
                inputType: 'password'
            }],

            // configs for BasicForm
            api: {
                submit: MainApi.login
            },
            clientValidation: true,
            paramsAsHash: true
        };
        Ext.apply(this, Ext.apply(this.initialConfig, config));
        Ext.ux.LoginForm.superclass.initComponent.apply(this, arguments);
    }//initComponent    
});


