

// Get list of candidate profiles
function $get_candidate_profiles(callback) {
    var req = {
        type: 'GET',
        url: $SCRIPT_ROOT + "/list",
        data: {}
    };
    $.ajax(req).done(function(response) {
        callback(response)
    }).fail(function(response2) {
        callback(response2);
    });
}


$( document ).ready(function() {
    $get_candidate_profiles( function(data) {
        console.log(data);
        $('#profiles_container').append('<table class="table table-hover" id="profiles_table"></table>');
        $('#profiles_table').append('<thead><tr id="header_row"></tr></thead>');
        $('#header_row').append('<th>#</th>');
        $('#header_row').append('<th>Profile Name</th>');
        $('#header_row').append('<th>Linkedin Public URL</th>');
        $('#header_row').append('<th>Sutro ID</th>');
        $('#profiles_table').append('<tbody id="table_body"></tbody>');
        for (i=0;i<data.profiles.length;i++) {
            row_head = '<th scope="row">'+data.profiles[i][6]+'</th>';
            row_name = '<td>'+data.profiles[i][1]+'</td>';
            row_url =  '<td><a href='+data.profiles[i][2]+' target="_blank" id='+data.profiles[i][0]+' class="linkedin_url_link">'+data.profiles[i][2]+'</a></td>';
            row_sutroid = '<td>'+data.profiles[i][0]+'</td>';
            $('#table_body').append('<tr>'+row_head+row_name+row_url+row_sutroid+'</tr>');
        }
        $('#loading_message').hide();
        $('.linkedin_url_link').click( function(e) {
            console.log(this.id);
            person_id = this.id;
            $.ajax({
                type: "GET",
                url: $SCRIPT_ROOT + "/candidate_click/",
                contentType: "application/json; charset=utf-8",
                data: { person_id: person_id },
                success: function(data) {
                    console.log('success: ',person_id);
                }
            });
        });
    });
});
