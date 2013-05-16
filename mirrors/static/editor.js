var install_markdown = function (data, content) {
    var typed_content = $("<textarea></textarea>").attr({
                        id: content.attr('id'),
                        name: content.attr('name')
                    });
    typed_content.text(data);
    content.after(typed_content).remove();
    /*
    content = typed_content;
    content.hallo({
        plugins: {
          'halloformat': {},
          'halloheadings': {},
          'hallolists': {},
          'halloreundo': {}
        }//,
        //toolbar: 'halloToolbarFixed'
      });
    */
    return typed_content;
}

$('window').ready(function(){
    var select = $('select[name=encoding]');
    var content = $('input[name=content]');
    var parent = content.parent();
    var link = parent.find('a');
    select.change(function() {
        switch(this.value) {
        case "md":
            if (link && link.attr('href')) {
                $.get(link.attr('href'), function(data) {
                    content = install_markdown(data, content);
                });
            } else {
                content = install_markdown('', content);
            }
            break;
        case "png":
            var typed_content = $("<input />").attr({
                                    id: content.attr('id'),
                                    type: 'file',
                                    name: content.attr('name')
                                });
            content.after(typed_content).remove();
            content = typed_content;
            break;
        }
    });
    select.trigger('change');
});
