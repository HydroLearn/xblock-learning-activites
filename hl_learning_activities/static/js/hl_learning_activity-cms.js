function Learning_Activity_Studio(runtime, xblock_element) {

    // extend from the default HLCK5 studio object
    // HL_TEXT_STUDIO.call(this, runtime, xblock_element);
    $(xblock_element).closest('.modal-window').addClass('hl_resize_correction');


    $(function($) {
        console.log('Initialized custom LA studio script.')


        console.log('children:')
        console.log(runtime.children(xblock_element));

        // to get child with specific Name
        // runtime.childMap(element, name)

        // cancel button clicked
        $(xblock_element).find('.cancel-button').bind('click', function() {
            runtime.notify('cancel', {});
        });



    })
}
