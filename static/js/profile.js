function getCsrfToken() {
    const cookie = document.cookie.split('; ').find(row => row.startsWith('csrf_access_token='));
    return cookie ? cookie.split('=')[1] : null;
}

function setupAjax() {
    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            const csrfToken = getCsrfToken();
            if (csrfToken) {
                xhr.setRequestHeader("X-CSRF-TOKEN", csrfToken);
            }
        }
    });
}

$(document).ready(function() {
    console.log("jQuery is loaded and DOM is ready!"); // Debugging
    setupAjax(); // Apply CSRF token to all AJAX requests

    $("#updateProfileBtn").click(function() {
        console.log("Edit Profile button clicked!"); // Debugging
        // Fetch current user data
        $.ajax({
            url: "/profile/get_profile/",
            type: "GET",
            success: function(userData) {
                // Pre-populate form with existing user data
                $("input[name='given_name']").val(userData.given_name || '');
                $("input[name='family_name']").val(userData.family_name || '');
                $("input[name='location']").val(userData.location || '');
                $("input[name='bio']").val(userData.bio || '');
                $("input[name='pronoun']").val(userData.pronoun || '');
                
                $("#profileModal").removeClass("hidden"); // Show modal
            },
            error: function(resp) {
                console.error("Failed to load user data", resp);
                alert("Failed to load your profile data. Please try again.");
            }
        });
    });    

    $("#closeModal").click(function() {
        $("#profileModal").addClass("hidden"); // Hide modal
    });

    $("#updateProfileForm").submit(function(e) {
        e.preventDefault();
        var formData = new FormData(this); // Use FormData to handle file upload

        $.ajax({
            url: "/profile/update/",
            type: "PATCH",
            headers: { "X-CSRF-TOKEN": getCsrfToken() },
            data: formData,
            contentType: false, // Prevent automatic content-type header
            processData: false, // Don't process FormData
            success: function(resp) {
                alert("Profile updated successfully!");
                location.reload(); // Reload page to see changes
            },
            error: function(resp) {
                console.log(resp);
                $("#profileError").text(resp.responseJSON?.error || "An error occurred").removeClass("hidden");
            }
        });
    });
});
