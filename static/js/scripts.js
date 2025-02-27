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
    
    setupAjax(); // Apply CSRF token to all AJAX requests

    $("form[name=signup_form]").submit(function(e) {
        e.preventDefault();
        var $form = $(this);
        var $error = $form.find(".error");
        var data = $form.serialize();

        $.ajax({
            url: "/user/signup",
            type: "POST",
            data: data,
            dataType: "json",
            success: function(resp) {
                window.location.href = "/user/login/";
            },
            error: function(resp) {
                console.log(resp);
                $error.text(resp.responseJSON?.error || "An error occurred").removeClass("error--hidden");
            }
        });
    });
    // Login 
    $("form[name=login_form]").submit(function(e) {
        e.preventDefault();
        var $form = $(this);
        var $error = $form.find(".error");
        var data = $form.serialize();

        $.ajax({
            url: "/user/login",
            type: "POST",
            data: data,
            dataType: "json",
            success: function(resp) {
                window.location.href = "/dashboard/";
            },
            error: function(resp) {
                console.log(resp);
                $error.text(resp.responseJSON?.error || "Invalid credentials").removeClass("error--hidden");
            }
        });
    });

    $("#logout_button").on("click", function() {
        console.log("Logout button clicked!"); // ✅ Force debug message

        const csrfToken = getCsrfToken(); // Get CSRF token
        console.log("Extracted CSRF Token:", csrfToken);  // ✅ Debugging log

        if (!csrfToken) {
            console.error("CSRF token is missing!");
            return;
        }

        $.ajax({
            url: "/user/logout",
            type: "POST",
            headers: {
                "X-CSRF-TOKEN": csrfToken // Send CSRF token in the request headers
            },
            success: function(resp) {
                console.log("Logout successful!");
                window.location.href = "/";
            },
            error: function(resp) {
                console.error("Logout Error:", resp.responseJSON || resp);
            }
        });
    });
    // Forgot password 
    $("#forgot_password_form").submit(function(e) {
        e.preventDefault();
        var email = $("#forgot_password_email").val();
        var csrfToken = getCsrfToken();

        console.log("Sending email:", email);  // Debugging log
        console.log("Extracted CSRF Token:", csrfToken);  // Debugging log

        $.ajax({
            url: "/user/request-password-reset",
            type: "POST",
            headers: { 
                "X-CSRF-TOKEN": csrfToken, 
                "Content-Type": "application/json"  
            },
            contentType: "application/json", 
            data: JSON.stringify({ email: email }),
            processData: false,  
            success: function(response) {
                console.log("Success Response:", response);
                alert("Password reset email sent!");
                window.location.href = "/";
            },
            error: function(response) {
                console.error("Error Response:", response);  // Debugging log
                alert("Error: " + (response.responseJSON?.error || "An error occurred"));
            }
        });
    });
    
    $("#reset_password_form").submit(function(e) {
        e.preventDefault();
        var token = $("#reset_password_token").val();
        var newPassword = $("#new_password").val();
        var confirmPassword = $("#confirm_password").val();

        $.ajax({
            url: "/user/reset-password/" + token,
            type: "POST",
            contentType: "application/json",
            data: JSON.stringify({
                new_password: newPassword,
                confirm_password: confirmPassword
            }),
            success: function(response) {
                alert("Password reset successful!");
                window.location.href = "/user/login/";
            },
            error: function(response) {
                alert("Error: " + response.responseJSON.error);
            }
        });
    });
});

function togglePassword(fieldId, toggleId) {
    var passwordField = document.getElementById(fieldId);
    var toggleButton = document.querySelector(`button[onclick*="${toggleId}"]`);

    if (passwordField.type === "password") {
        passwordField.type = "text";
        toggleButton.textContent = "Hide";
    } else {
        passwordField.type = "password";
        toggleButton.textContent = "Show";
    }
}