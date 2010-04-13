
<%@ page import="testapp.Company" %>
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
        <meta name="layout" content="main" />
        <g:set var="entityName" value="${message(code: 'company.label', default: 'Company')}" />
        <title><g:message code="default.list.label" args="[entityName]" /></title>
    </head>
    <body>
        <div class="nav">
            <span class="menuButton"><a class="home" href="${createLink(uri: '/')}"><g:message code="default.home.label"/></a></span>
            <span class="menuButton"><g:link class="create" action="create"><g:message code="default.new.label" args="[entityName]" /></g:link></span>
        </div>
        <div class="body">
            <h1><g:message code="default.list.label" args="[entityName]" /></h1>
            <g:if test="${flash.message}">
            <div class="message">${flash.message}</div>
            </g:if>
            <div class="list">
                <table>
                    <thead>
                        <tr>
                        
                            <g:sortableColumn property="id" title="${message(code: 'company.id.label', default: 'Id')}" />
                        
                            <g:sortableColumn property="startDate" title="${message(code: 'company.startDate.label', default: 'Start Date')}" />
                        
                            <g:sortableColumn property="name" title="${message(code: 'company.name.label', default: 'Name')}" />
                        
                            <g:sortableColumn property="endDate" title="${message(code: 'company.endDate.label', default: 'End Date')}" />
                        
                            <g:sortableColumn property="purpose" title="${message(code: 'company.purpose.label', default: 'Purpose')}" />
                        
                            <g:sortableColumn property="notes" title="${message(code: 'company.notes.label', default: 'Notes')}" />
                        
                        </tr>
                    </thead>
                    <tbody>
                    <g:each in="${companyInstanceList}" status="i" var="companyInstance">
                        <tr class="${(i % 2) == 0 ? 'odd' : 'even'}">
                        
                            <td><g:link action="show" id="${companyInstance.id}">${fieldValue(bean: companyInstance, field: "id")}</g:link></td>
                        
                            <td><g:formatDate date="${companyInstance.startDate}" /></td>
                        
                            <td>${fieldValue(bean: companyInstance, field: "name")}</td>
                        
                            <td><g:formatDate date="${companyInstance.endDate}" /></td>
                        
                            <td>${fieldValue(bean: companyInstance, field: "purpose")}</td>
                        
                            <td>${fieldValue(bean: companyInstance, field: "notes")}</td>
                        
                        </tr>
                    </g:each>
                    </tbody>
                </table>
            </div>
            <div class="paginateButtons">
                <g:paginate total="${companyInstanceTotal}" />
            </div>
        </div>
    </body>
</html>
