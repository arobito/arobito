/*
    Copyright 2014 The Arobito Project

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
*/

(function ($, robi) {
    "use strict";

    var local = {};
    local.clientKey = null;

    robi.error = function(title, message) {
        $.growl.error({ message: message, title: title });
    };

    robi.warn = function(title, message) {
        $.growl.warning({ message: message, title: title });
    };
    
    robi.notice = function(title, message) {
        $.growl.notice({ message: message, title: title });
    };

    robi.message = function(title, message) {
        $.growl({ message: message, title: title });
    };

    robi.isLoggedIn = function () {
        return (null !== local.clientKey);
    };
    
    local.loadPagelet = function(container, pagelet) {
        $(container).load('/static/pagelets/' + pagelet + '.html',
            function (response, status, xhr) {
                if (status === 'error') {
                    robi.error('Pagelet load error', 'Failed to load pagelet \'' + pagelet + '\'');
                }
            });
    };
    
    robi.statusPage = function() {
        local.loadPagelet('#application', 'status');
    };
    
    local.login = function(data) {
        if (!(data.auth)) {
            robi.error('Login failed', 'Unknown answer received from server!');
            return;
        }
        if ((!(data.auth.success)) || (false === data.auth.success)) {
            robi.warn('Login failed', data.auth.reason);
            return;
        }
        if (true === data.auth.success) {
            local.clientKey = data.auth.key;
            $('#loginForm').css('display', 'none');
            $('#navigationBlock').css('display', 'block');
            robi.notice('Login successful', 'Thank you, have fun!');
            robi.statusPage();
            return;
        }
        robi.warn('Login failed', 'Failed for an unknown reason.');
    };
    
    local.logout = function(data) {
        local.clientKey = null;
        $('#navigationBlock').css('display', 'none');
        $('#loginForm').css('display', 'block');
        robi.notice('Logout successful', 'Good bye!');
        robi.statusPage();
    };

    local.shutdown = function(data) {
        if (data.shutdown) {
            robi.notice('Shutdown request sent', 'Robi is shutting down.');
        }
        else {
            robi.error('Shutdown request failed', 'Robi is not shutting down. Sorry.');
        }
    };
    
    local.getSessionCount = function (data) {
        // TODO
    };
    
    robi.login = function(f) {
        var username = $(f).find('input[name="username"]').val(),
            password = $(f).find('input[name="password"]').val(),
            target = $(f).attr('action');
        $(f).find('input[name="password"]').val('');
        $.ajax(target, {
            data: JSON.stringify({ username: username, password: password }),
            success: function (data, status, xhr) {
                local.login(data);
            },
            error: function (xhr, status, errorThrown) {
                robi.error('Error logging in', 'An error occurred while logging in: ' + errorThrown);
            }
        });
    };
    
    robi.logout = function() {
        $.ajax('/app/logout', {
            data: JSON.stringify({ key: local.clientKey }),
            success: function (data, status, xhr) {
                local.logout(data);
            },
            error: function (xhr, status, errorThrown) {
                robi.error('Error logging out', 'An error occurred while logging out: ' + errorThrown);
            }
        });
    };

    robi.shutdown = function() {
        $.ajax('/app/shutdown', {
            data: JSON.stringify({ key: local.clientKey }),
            success: function (data, status, xhr) {
                local.shutdown(data);
            },
            error: function (xhr, status, errorThrown) {
                robi.error('Shutdown Error', 'An error occurred while shutting down: ' + errorThrown);
            }
        });
    };
    
    robi.getSessionCount = function () {
        $.ajax('/app/get_session_count', {
            data: JSON.stringify({ key: local.clientKey }),
            success: function (data, status, xhr) {
                local.getSessionCount(data);
            },
            error: function (xhr, status, errorThrown) {
                robi.error('GetSessionCount Error', 'An error occurred while getting the session count: ' + errorThrown);
            }
        });
    };
    
    local.initLoginForm = function() {
	$('#loginForm').find('form input').each(function(obj) {
	    $(obj).addClass('ui-corner-all');
	});
        $('#loginForm').find('form').submit(function (evtObj) {
            robi.login($(this));
            return false;
        });
    };
    
    local.initMainToolbar = function() {
        $('#mtPageStatusButton').button({
            text: true,
            icons: {
                primary: 'ui-icon-home'
            }
        }).click(function() {
            robi.statusPage();
        });
        $('#mtLogoutButton').button({
            text: true,
            icons: {
                primary: 'ui-icon-close'
            }
        }).click(function() {
            robi.logout();
        });
    };
    
    local.init = function() {
        $.ajaxSetup({
            cache: false,
            dataType: 'json',
            async: true,
            crossDomain: false,
            type: 'POST',
            contentType: 'application/json; charset=utf-8'
        });
        $(document).ready(function () {
            robi.statusPage();
            local.initLoginForm();
            local.initMainToolbar();
        });
    };
    
    local.init();
    
})(jQuery, window.robi = window.robi || {});
