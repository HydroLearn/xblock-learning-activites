function experiment_XBlock(runtime, element) {


    // with studio editable the styling isn't perfect for the fully resizable modal
    //      additional styling will be needed
    //      before incorporating this functionality
    //
    //$(element).closest('.modal-window').addClass('hl_resize_correction');
    //$('body').trigger('resize_modal')

    var Studio_editable_mixin = new StudioEditableXBlockMixin(runtime, element);





}