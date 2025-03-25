$(document).ready(function() {
    console.log("JavaScript Loaded");

    // Button Hover Effect
    $(".btn").hover(
        function() {
            $(this).css("opacity", "0.8");
        },
        function() {
            $(this).css("opacity", "1");
        }
    );

    // Dark Mode Toggle
    $("#dark-mode-toggle").click(function() {
        $("body").toggleClass("dark-mode");
    });

    // AJAX Login
    $("#login-form").submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "/login/",
            data: {
                username: $("#username").val(),
                password: $("#password").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
                if (response.success) {
                    window.location.href = "/";
                } else {
                    $("#login-message").text("Invalid credentials, try again!");
                }
            }
        });
    });

    // AJAX Signup
    $("#signup-form").submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "/signup/",
            data: {
                username: $("#signup-username").val(),
                email: $("#signup-email").val(),
                password: $("#signup-password").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
                if (response.success) {
                    window.location.href = "/";
                } else {
                    $("#signup-message").text("Error: " + response.error);
                }
            }
        });
    });

    // AJAX for Booking a Class
    $("#book-class-form").submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "/book-class/",
            data: {
                class_id: $("#class-id").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
                if (response.success) {
                    $("#booking-message").text("Class booked successfully!");
                } else {
                    $("#booking-message").text("Failed to book class.");
                }
            }
        });
    });

    // AJAX for Booking an Activity
    $("#book-activity-form").submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "/book-activity/",
            data: {
                activity_id: $("#activity-id").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
                if (response.success) {
                    $("#activity-message").text("Activity booked successfully!");
                } else {
                    $("#activity-message").text("Failed to book activity.");
                }
            }
        });
    });

    // AJAX for Submitting Feedback
    $("#feedback-form").submit(function(e) {
        e.preventDefault();

        $.ajax({
            type: "POST",
            url: "/feedback/",
            data: {
                message: $("#feedback-message").val(),
                csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val()
            },
            success: function(response) {
                if (response.success) {
                    $("#feedback-response").text("Thank you for your feedback!");
                } else {
                    $("#feedback-response").text("Error submitting feedback.");
                }
            }
        });
    });
});
