$(document).ready(function(){
    spinner = '<div id="mdb-preloader" class="flex-center"><div id="preloader-markup"></div></div>'
    $.get('/portfolio/ideas_app/bright_ideas/list', function(data){
        //console.log('IDEAS: ', data)
        $('#ideas-list').html(spinner);
        $('#ideas-list').html(data);
    });
    $.get('/portfolio/user/first_name', function(first_name){
        if(first_name === 'GUEST'){
            //console.log('NOT SIGNED IN!')
        } else {
            //console.log('FIRST_NAME: ', first_name)
            $('#user-first-name').html(first_name);
            $('#user-first-name2').html(first_name);
        }
    });
    // $.get('/portfolio/ideas_app/bright_ideas/' + CURRENT_IDEA_ID, function(idea){
    //     console.log()
    //     $('#idea').html(idea);
    // })
    $('#idea-create-form').submit(function(e){
        console.log('BEFORE SUBMIT')
        spinner = '<div id="mdb-preloader" class="flex-center"><div id="preloader-markup"></div></div>'
        e.preventDefault()
        $.ajax({
            url: '/portfolio/ideas_app/bright_ideas/create',
            method: 'POST',
            data: $('#idea-create-form').serialize(),
            success: function(){
                console.log('SUCCESS')
                $.get('/portfolio/ideas_app/bright_ideas/list', function(data){
                    //console.log('IDEAS: ', data)
                    $('#ideas-list').html(data);
                })
                // $('#alerts').html(data.responseText)
                $('#idea-create-form input, #idea-create-form textarea').val('')
            },
            error: function(data) {
                // console.log('ERROR', data)
                $('#alerts').html(data.responseText)
            }
        })
    })
    $('#user-update-form').submit(function(e) {
        e.preventDefault()
        $.ajax({
            url: '/portfolio/user/update/' + CURRENT_USER_ID,
            method: 'POST',
            data: $('#user-update-form').serialize(),
            success: function(alerts) {
                console.log('SUCCESS')
                // $('.btn-profile-update').html('<span class="spinner-border spinner-border-sm mr-2" role="status" aria-hidden="true"></span>Saving...').addClass('disabled');
                $("#alerts-info").html(alerts)
            },
            error: function(data) {
                console.log('ERROR')
                $("#alerts").html(data.responseText)
            }
        })
    });
})