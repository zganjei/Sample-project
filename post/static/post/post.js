$(document).ready(function () {
    for (let i in CKEDITOR.instances) {

        let editor = CKEDITOR.instances[i];
        // editor.resize(220, 220);
        // makeContexMenu2(editor);

        CKEDITOR.config.mentions = [
            {
                // feed: function (options, callback) {
                //     console.log(options);
                //     console.log(callback);
                // },
                // feed: ['یزید'],
                feed: '/hashtag-list?query={encodedQuery}',
                marker: '#',
                minChars: 2,
                pattern: /\#[a-zA-Z0-9ا-ی]*$/,
                itemTemplate: '<li data-id="{id}">{name}</li>',
                // outputTemplate: `<a href="/tracker/{name}">{name}</a>`
            },

        ];


    }
});

function makeContexMenu2(editor) {
    editor.on('instanceReady', function (e) {
// Register a command execute on context menu item click
        editor.addCommand('test1', {
            exec: editor => {
                // let dialogObj = new CKEDITOR.dialog(editor2, 'smiley');
                // dialogObj.show();
                console.log(editor.getSelection().getRanges()[0].extractContents());
                // console.log(alert(!!CKEDITOR.dtd['p']['span']));
                let selection = editor.getSelection();
                editor.insertHtml('<input type="hidden" name="tags" value="tag1,tag2,tag3"/>');
                // console.log(selection.getType());
                // alert('test1');
            }
        });

        // Check for context menu and add new item/s
        if (editor.contextMenu) {
            // Add group and item/s
            editor.addMenuGroup('testGroup');
            editor.addMenuItem('testItem', {
                label: 'اضافه کردن تگ',
                icon: this.path + 'icons/test.png',
                command: 'test1',
                group: 'testGroup'
            });

            // Add event listener
            editor.contextMenu.addListener(element => {
                console.log(element);
                return {testItem: CKEDITOR.TRISTATE_OFF};
            });
        }
    });
}

function makeContexMenu1(editor) {
    editor.on('instanceReady', function (e) {
        // editor.resize(200, 200);

        editor.addCommand("myCommand", {
            exec: function (editor) {
                alert("myCommand");
            }
        });

        var myCommand = {
            label: editor.lang.image.menu,
            command: 'myCommand',
            group: 'image'
        };


        editor.contextMenu.addListener(function (element, selection) {
            return {
                myCommand: CKEDITOR.TRISTATE_OFF
            };
        });

        editor.addMenuItems({
            myCommand: {
                label: editor.lang.image.menu,
                command: 'myCommand',
                group: 'image',
                order: 1
            }
        });
    });
}