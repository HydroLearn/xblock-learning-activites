function Learning_Activity(runtime, xblock_element) {

    // extend from the default HLCK5 studio object
    // HL_TEXT_STUDIO.call(this, runtime, xblock_element);


    $(function($) {

        console.log('Initialized custom LA lms script.')

        console.log('children:')
        console.log(runtime.children(xblock_element));



    })
}
