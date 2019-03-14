function Learning_Activity_Studio(runtime, element) {

    // initialize the studio editable mixin which will handle the 'editable_fields'
    // and enable saving for those
    var Studio_editable_mixin = new StudioEditableXBlockMixin(runtime, element);

    // extend from the default HLCK5 studio object
    // HL_TEXT_STUDIO.call(this, runtime, element);
    // $(element).closest('.modal-window').addClass('hl_resize_correction');


    $(function($) {
        console.log('Initialized custom LA studio script.')


        console.log('children:')
        console.log(runtime.children(element));

        // to get child with specific Name
        // runtime.childMap(element, name)

        // cancel button clicked
        $(element).find('.cancel-button').bind('click', function() {
            runtime.notify('cancel', {});
        });



    })
}
