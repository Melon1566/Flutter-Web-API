import mysql.connector
from flask import Flask, jsonify, request
from flask_cors import CORS
import simplejson as json
import datetime as datetime
from datetime import timedelta
import requests
import secrets
import mailchimp_transactional as MailchimpTransactional
from mailchimp_transactional.api_client import ApiClientError
import concurrent.futures
import operator
import helpers

# OUR SOURCE FILES
import users
import checklists
import vendors
import infractionType
import daType
import rewards
import responsibilities
import databaseDetails
import accountabilityReportingHome
import accountabilityReportingInfractionsByDay
import accountabilityReportingTotalAccountability
import accountabilityReportingInfractionsByWeek
import rolesAndUsers
import password
import images
import shifts
import notification
import disciplinaryActions
import task
import dashboardToDoList
import forms
import waste
import wasteScreen
import points
import vendorBridgeAPI
import dashboardTasks
import dashboardPoints
import dashboardCheckin


accountsEndpoint = "vsbl-prod.cluster-ch0dsenirhlb.us-east-1.rds.amazonaws.com"


def defaultconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


################IF running locally copy the section below and replace above the first if statement################################################
""" 

app = Flask(__name__)
CORS(app)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/AppDataHandler', methods=['POST', 'GET'])
def requestHandler():
    requestData = request.get_json() 

"""


##################################################################


# IF deploying to production, lambda use this code section to declare the handler otherwise use the above section without passed parameters
""" 
def requestHandler(event, context):
    body = ""
    if(event.get("body") is bytes):
        body = event.get("body").decode("utf-8")
    else:
        body = event.get("body")
    
    requestData = json.loads(body) 
"""
######################################################################################

def requestHandler(event, context):
    body = ""
    if(event.get("body") is bytes):
        body = event.get("body").decode("utf-8")
    else:
        body = event.get("body")
    
    requestData = json.loads(body) 


    ###################################################################################
    #############################Waste Screen function routing#######################################
    if requestData['RequestType'] == "GetWaste":
        print("Getting Waste")
        return wasteScreen.getWaste(requestData['Data'], False)
    elif requestData['RequestType'] == "UpdateWaste":
        print("Updating Waste Data")
        return wasteScreen.updateWaste(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteFilterInfo":
        print("Getting Waste Filter Info")
        return wasteScreen.getWasteFilterInfo(requestData['Data'])
    elif requestData['RequestType'] == "UpdateProductInfo":
        print("Getting Waste Filter Info")
        return wasteScreen.updateProductInfo(requestData['Data'])
    elif requestData['RequestType'] == "GetProducts":
        print("Getting Product List")
        return wasteScreen.getProducts(requestData['Data'])

    #############################User function routing#######################################
    elif requestData['RequestType'] == "GetUsers":
        print('getting users')
        return users.getUsers(requestData['Data'])
    elif requestData['RequestType'] == "GetLeaderBoard":
        return users.getLeaderBoard(requestData['Data'])
    elif requestData['RequestType'] == "SaveUserSettings":
        print("Saving User Settings")
        return users.saveUserSettings(requestData['Data'])
    elif requestData['RequestType'] == "GetProfileSummaryTabData":
        print("Getting DA Reporting Data")
        return users.getProfileSummaryTabData(requestData['Data'])
    elif requestData['RequestType'] == "GetLocalID":
        print("Getting local id")
        return users.getLocalUserID(requestData['Data'])
    elif requestData['RequestType'] == "GetUserProfile":
        print("Getting User Profile")
        return users.getUserProfile(requestData['Data'])
    elif requestData['RequestType'] == "GetUserProfileSummaryData":
        print("Getting User Profile Summary Data")
        return users.getUserProfileSummaryData(requestData['Data'])
    elif requestData['RequestType'] == "Login":
        print("Logging in")
        return users.login(requestData['Data'])
    elif requestData['RequestType'] == "GetInfractionUsers":
        return users.getInfractionUsers(requestData['Data'])
    elif requestData['RequestType'] == "UploadProfilePicture":
        print("Uploading Profile Picture")
        return users.uploadProfilePicture(requestData['Data'])  # users
    elif requestData['RequestType'] == "GetProfilePicture":
        print("Get Profile Picture")
        return users.getProfilePicture(requestData['Data'])

    ###########################################################################################

    #############################Checklist function routing#######################################
    elif requestData['RequestType'] == "GetChecklistTemplate":
        print('fetching checklist template')
        return checklists.getChecklistTemplate(requestData['Data'])
    elif requestData['RequestType'] == "GetChecklistTemplateList":
        return checklists.getChecklistTemplateList(requestData['Data'])
    elif requestData['RequestType'] == "CreateNewChecklistSubmission":
        return checklists.createNewChecklistSubmission(requestData['Data'])
    elif requestData['RequestType'] == "GetChecklistSubmissionList":
        return checklists.getChecklistSubmissionList(requestData['Data'])
    elif requestData['RequestType'] == "GetChecklistSubmissionData":
        return checklists.getChecklistSubmissionData(requestData['Data'])
    elif requestData['RequestType'] == "SaveChecklistSubmission":
        return checklists.saveCheckListSubmission(requestData['Data'])
    elif requestData['RequestType'] == "DeleteChecklistSubmission":
        return checklists.deleteChecklistSubmission(requestData['Data'])
    elif requestData['RequestType'] == "SaveChecklistTemplate":
        return checklists.saveChecklistTemplate(requestData['Data'])
    elif requestData['RequestType'] == "DeleteChecklistTemplate":
        return checklists.deleteChecklistTemplate(requestData['Data'])
    elif requestData['RequestType'] == "GetTemplateActivity":
        return checklists.getChecklistTemplateActivity(requestData['Data'])
    elif requestData['RequestType'] == "CompleteChecklistSubmission":
        return checklists.completeChecklistSubmission(requestData['Data'])
    elif requestData['RequestType'] == "GetChecklistReportingData":
        return checklists.getChecklistReportingData(requestData['Data'])
    elif requestData['RequestType'] == "GetMyChecklistsList":
        print("Getting my checklists")
        return checklists.getMyChecklistList(requestData['Data'])
    elif requestData['RequestType'] == "ReassignChecklist":
        print("Reassigning Checklist")
        return checklists.reassignChecklist(requestData['Data'])
    elif requestData['RequestType'] == "GetUserChecklistReportingData":
        return checklists.getUserChecklistReportingData(requestData['Data'])
    elif requestData['RequestType'] == "GetChecklistQuestionSearchList":
        return checklists.getChecklistQuestionSearchList(requestData['Data'])
    elif requestData['RequestType'] == "GetChecklistReportingCompletionOverTimeData":
        return checklists.getChecklistCompletionOverTimeData(requestData['Data'])
    elif requestData['RequestType'] == "GetChecklistActionableTasks":
        print("Getting Checklist Actionable Tasks")
        return checklists.getChecklistActionableTasks(requestData['Data'])

    ############################################################################

    #############################Points function routing#######################################
    elif requestData['RequestType'] == "AssignPoints":
        print("Assigning Points")
        return points.assignPoints(requestData['Data'])  # Points

    #############################Vendor function routing#######################################
    elif requestData['RequestType'] == "GetVendors":
        return vendors.getVendors(requestData['Data'])
    elif requestData['RequestType'] == "AddVendor":
        return vendors.addVendor(requestData['Data'])
    elif requestData['RequestType'] == "UpdateVendor":
        return vendors.updateVendor(requestData['Data'])
    elif requestData['RequestType'] == "DeleteVendor":
        return vendors.deleteVendor(requestData['Data'])

    ###########################################################################################

    ############################Infraction Type Function Routing##############################
    elif requestData['RequestType'] == "DeleteInfraction":
        return infractionType.deleteInfraction(requestData['Data'])
    elif requestData['RequestType'] == "UpdateInfraction":
        return infractionType.updateInfraction(requestData['Data'])
    elif requestData['RequestType'] == "AddInfractionType":
        return infractionType.addInfractionType(requestData['Data'])
    elif requestData['RequestType'] == "GetUserProfileInfractions":
        print("Geting Profile Infractions")
        return infractionType.getUserProfileInfractions(requestData['Data'])
    elif requestData['RequestType'] == "GetInfractionDetails":
        return infractionType.getInfractionDetails(requestData['Data'])
    elif requestData['RequestType'] == "UpdateInfractionDetails":
        return infractionType.updateInfractionDetails(requestData['Data'])
    elif requestData['RequestType'] == "DeleteUserInfraction":
        return infractionType.deleteUserInfraction(requestData['Data'])
    elif requestData['RequestType'] == "GetInfractionTypeList":
        print("Getting Infraction List")
        return infractionType.getInfractionTypeList(requestData['Data'])
    elif requestData['RequestType'] == "AssignInfraction":
        print("Getting Infraction List")
        return infractionType.assignInfraction(requestData['Data'])

    ###########################################################################################

    ############################Disciplinary Action Type Function Routing#####################
    elif requestData['RequestType'] == "GetDisciplinaryActionTypeList":
        return daType.getDisciplinaryActionTypeList(requestData['Data'])
    elif requestData['RequestType'] == "AddDisciplinaryActionType":
        return daType.addDisciplinaryActionType(requestData['Data'])
    elif requestData['RequestType'] == "UpdateDisciplinaryActionType":
        return daType.updateDisciplinaryActionType(requestData['Data'])
    elif requestData['RequestType'] == "DeleteDisciplinaryActionType":
        return daType.deleteDisciplinaryActionType(requestData['Data'])

    ###########################################################################################

    ############################Rewards Function Routing######################################
    elif requestData['RequestType'] == "GetRecognitionRewardsType":
        return rewards.getRecognitionRewards(requestData['Data'])
    elif requestData['RequestType'] == "AddRecognitionRewardType":
        return rewards.addRecognitionReward(requestData['Data'])
    elif requestData['RequestType'] == "UpdateRecognitionRewardType":
        return rewards.updateRecognitionRewardType(requestData['Data'])
    elif requestData['RequestType'] == "DeleteRecognitionRewardType":
        return rewards.deleteRecognitionRewardType(requestData['Data'])
    elif requestData['RequestType'] == "GetPointLogItem":
        print("Getting Point Log Item")
        return rewards.getPointLogItem(requestData['Data'])
    elif requestData['RequestType'] == "GetPendingRewardsLog":
        print("GetPendingRewardLog")
        return rewards.getPendingRewardsLog(requestData['Data'])
    elif requestData['RequestType'] == "GetRewardReviewData":
        print("Getting reward data for review")
        return rewards.getRewardReviewData(requestData['Data'])
    elif requestData['RequestType'] == "ReassignRewardReview":
        print("Reassign Reward Review")
        return rewards.reassignRewardReview(requestData['Data'])
    elif requestData['RequestType'] == "CompleteRewardReview":
        print("Complete Reward Review")
        return rewards.completeRewardReview(requestData['Data'])
    elif requestData['RequestType'] == "RedeemReward":
        print("Redeeming Reward")
        return rewards.redeemReward(requestData['Data'])

    ###########################################################################################

    ############################Responsibility Function Routing###############################
    elif requestData['RequestType'] == "GetResponsibilities":
        return responsibilities.getResponsibilities(requestData['Data'])
    elif requestData['RequestType'] == "AddResponsibility":
        return responsibilities.addResponsibility(requestData['Data'])
    elif requestData['RequestType'] == "UpdateResponsibility":
        return responsibilities.updateResponsibility(requestData['Data'])
    elif requestData['RequestType'] == "DeleteResponsibility":
        return responsibilities.deleteResponsibility(requestData['Data'])

    ###########################################################################################

    ############################Database Function Routing#####################################
    elif requestData['RequestType'] == "GetDatabaseDetails":
        return databaseDetails.getDatabaseDetails(requestData['Data'])
    elif requestData['RequestType'] == "UploadDatabaseImage":
        return databaseDetails.uploadDatabaseProfilePicture(requestData['Data'])
    elif requestData['RequestType'] == "SendBroadcast":
        return databaseDetails.sendBroadcast(requestData['Data'])
    elif requestData['RequestType'] == "GetUserDatabaseList":
        print("Getting User Databases")
        return databaseDetails.getUserDatabaseList(requestData['Data'])
    elif requestData['RequestType'] == "SetPrimaryDatabase":
        print("Setting Primary Database")
        return databaseDetails.setPrimaryDatabase(requestData['Data'])

    ###########################################################################################

     ############################Role & Users Function Routing#####################################
    elif requestData['RequestType'] == "GetRolesList":
        print("Getting Roles List")
        return rolesAndUsers.getRolesList(requestData['Data'])
    elif requestData['RequestType'] == "AddRole":
        print("Adding Role")
        return rolesAndUsers.addRole(requestData['Data'])
    elif requestData['RequestType'] == "GetRoleUsers":
        print("Getting Role Users")
        return rolesAndUsers.getRoleUsers(requestData['Data'])
    elif requestData['RequestType'] == "GetRolePermissions":
        print("Getting Role Permissions")
        return rolesAndUsers.getRolePermissions(requestData['Data'])
    elif requestData['RequestType'] == "SaveRoleSettings":
        print("Saving Role Settings")
        return rolesAndUsers.saveRoleSettings(requestData['Data'])
    elif requestData['RequestType'] == "GetUserPermissions":
        print("Getting User Permissions")
        return rolesAndUsers.getUserPermissions(requestData['Data'])
    elif requestData['RequestType'] == "SaveUserPermissions":
        print("Saving User Permissions")
        return rolesAndUsers.saveUserPermissions(requestData['Data'])
    elif requestData['RequestType'] == "ChangeUserRole":
        print("Changing User Role")
        return rolesAndUsers.changeUserRole(requestData['Data'])
    elif requestData['RequestType'] == "DeleteRole":
        print("Deleting Role")
        return rolesAndUsers.deleteRole(requestData['Data'])
    elif requestData['RequestType'] == "GetUserRole":
        print("Getting Role")
        return rolesAndUsers.getUserRole(requestData['Data'])
    elif requestData['RequestType'] == "SetRolePermission":
        print("Setting Role Permission")
        return rolesAndUsers.setRolePermission(requestData['Data'])
    elif requestData['RequestType'] == "GetNonRoleUsers":
        print("Getting Users not in role")
        return rolesAndUsers.getUsersNotInRole(requestData['Data'])
    elif requestData['RequestType'] == "AddUsersToRole":
        print("Add users to role")
        return rolesAndUsers.addUsersToRole(requestData['Data'])

    ###########################################################################################

    ############################Password Function Routing#####################################

    elif requestData['RequestType'] == "ResetPassword":
        print("Getting Role")
        return password.resetPassword(requestData['Data'])
    elif requestData['RequestType'] == "SendPasswordResetEmail":
        print("Sending reset email")
        return password.sendPasswordResetEmail(requestData['Data'])

    ###########################################################################################

    ############################Image Function Routing#####################################
    elif requestData['RequestType'] == "SaveImage":
        print("Saving Image")
        return images.saveImage(requestData['Data'])
    elif requestData['RequestType'] == "GetImages":
        print("Getting Images")
        return images.getImages(requestData['Data'])
    elif requestData['RequestType'] == "DeleteImage":
        print("Delete Image")
        return images.deleteImage(requestData['Data'])

    ###########################################################################################

    ############################Shift Function Routing#####################################
    elif requestData['RequestType'] == "CreateShiftGroup":
        print("Creating Shift Group")
        return shifts.createShiftGroup(requestData['Data'])
    elif requestData['RequestType'] == "GetShiftGroups":
        print("Getting Shift Groups")
        return shifts.getShiftGroups(requestData['Data'])
    elif requestData['RequestType'] == "SaveShiftDetails":
        print("Saving Shift Template")
        return shifts.saveShiftTemplate(requestData['Data'])
    elif requestData['RequestType'] == "GetShiftTemplateData":
        print("Getting Shift Template Data")
        return shifts.getShiftTemplateData(requestData['Data'])
    elif requestData['RequestType'] == "UpdateShiftGroup":
        print("Updating Shift Group")
        return shifts.editShiftGroupData(requestData['Data'])
    elif requestData['RequestType'] == "UpdateShiftActiveStatus":
        print("Update Shift Active Status")
        return shifts.updateShiftActiveStatus(requestData['Data'])
    elif requestData['RequestType'] == "DeleteShiftGroup":
        print("Deleting Shift Group")
        return shifts.deleteShiftGroup(requestData['Data'])
    elif requestData['RequestType'] == "GetShiftSubmissionData":
        print("Deleting Shift Group")
        return shifts.getShiftSubmissionData(requestData['Data'])
    elif requestData['RequestType'] == "AssignAndCreateShiftSubmission":
        print("Creating Shift Submission")
        return shifts.assignAndCreateShiftSubmission(requestData['Data'])
    elif requestData['RequestType'] == "GetShiftSubmissionToDoList":
        print("Creating Shift Submission")
        return shifts.getShiftToDoList(requestData['Data'])
    elif requestData['RequestType'] == "GetSafeCountData":
        print("Getting Safe Count Data")
        return shifts.getSafeCountData(requestData['Data'])
    elif requestData['RequestType'] == "SaveSafeCount":
        print("Saving Safe Count")
        return shifts.saveSafeCount(requestData['Data'])
    elif requestData['RequestType'] == "AddSafeCount":
        print("Adding Safe Count")
        return shifts.addSafeCount(requestData['Data'])
    elif requestData['RequestType'] == "CompleteShift":
        print("Complete Shift")
        return shifts.completeShift(requestData['Data'])
    elif requestData['RequestType'] == "GetShiftSubmission":
        print("Getting Shift Submission")
        return shifts.getShiftSubmission(requestData['Data'])
    elif requestData['RequestType'] == "GetShiftVerifyWasteData":
        print("Getting Shift Waste Data")
        return shifts.getShiftVerifyWasteData(requestData['Data'])
    elif requestData['RequestType'] == "GetVerifyWasteShiftDetails":
        print("Getting Shift Details")
        return shifts.getVerifyWasteShiftDetails(requestData['Data'])
    elif requestData['RequestType'] == "VerifyWasteData":
        print("Verifying Waste")
        return shifts.verifyWasteData(requestData['Data'])
    elif requestData['RequestType'] == "ReassignShift":
        print("Reassigning Shift")
        return shifts.reassignShift(requestData['Data'])

    ###########################################################################################

    ############################Notification Function Routing#####################################
    elif requestData['RequestType'] == "SetPushToken":
        print("Setting Push Token")
        return notification.setNotificationToken(requestData['Data'])
    elif requestData['RequestType'] == "GetNotificationFeed":
        print("Getting Notification Feed")
        return notification.getNotificationFeed(requestData['Data'])
    elif requestData['RequestType'] == "SetReadNotificationStatus":
        print("Setting Read Status")
        return notification.setNotificationReadStatus(requestData['Data'])
    elif requestData['RequestType'] == "MarkAllAsRead":
        print("Marking as read")
        return notification.markAllAsRead(requestData['Data'])

    ###########################################################################################

    ############################Dashboard Function Routing#####################################
    elif requestData['RequestType'] == "GetDashboardToDoList":
        print("getting to do list")
        return getDashboardToDoList(requestData['Data'])
    elif requestData['RequestType'] == "GetChecklistDashboardSubmissionList":
        print("Getting Checklist Dashboard")
        return getChecklistDashboardList(requestData['Data'])

    ###########################################################################################

    ############################Disciplinary Action Function Routing#####################################
    elif requestData['RequestType'] == "GetDisciplinaryActionDetails":
        print("Getting DA Details")
        return disciplinaryActions.getDisciplinaryActionDetails(requestData['Data'])
    elif requestData['RequestType'] == "GetDisciplinaryActionDetailInfractionList":
        print("Gettin DA Infractions")
        return disciplinaryActions.getDisciplinaryActionDetailInfractionList(requestData['Data'])
    elif requestData['RequestType'] == "UpdateDisciplinaryActionDetails":
        print("Updating DA Details")
        return disciplinaryActions.updateDisciplinaryActionDetails(requestData['Data'])
    elif requestData['RequestType'] == "ReassignDisciplinaryAction":
        print("Updating DA Details")
        return disciplinaryActions.reassignDisciplinaryAction(requestData['Data'])
    elif requestData['RequestType'] == "GetAccountabilityLog":
        print("Getting Accountability Log")
        return disciplinaryActions.getAccountabilityLog(requestData['Data'])
    elif requestData['RequestType'] == "GetUserProfileDAs":
        print("Geting Profile Disciplinary Actions")
        return disciplinaryActions.getUserProfileDisciplinaryActions(requestData['Data'])
    elif requestData['RequestType'] == "GetDAContributingFactors":
        return disciplinaryActions.getDAContributingFactors(requestData['Data'])
    elif requestData['RequestType'] == "AssignDisciplinaryAction":
        print("Assigning Disciplinary Action")
        return disciplinaryActions.assignDisciplinaryAction(requestData['Data'])

    ###########################################################################################

    ############################Task Function Routing#####################################
    elif requestData['RequestType'] == "DeleteTask":
        print("Deleting Task")
        return task.deleteTask(requestData['Data'])
    elif requestData['RequestType'] == "UpdateTask":
        print("Updating Task")
        return task.updateTask(requestData['Data'])
    elif requestData['RequestType'] == "AssignTask":
        print("Assigning Task")
        return task.assignTask(requestData['Data'])
    elif requestData['RequestType'] == "GetTaskData":
        print("Get Task Data")
        return task.getTaskData(requestData['Data'])
    elif requestData['RequestType'] == "CompleteTask":
        print("Completing Task")
        return task.completeTask(requestData['Data'])

    ###########################################################################################

    ############################Form Function Routing#####################################
    elif requestData['RequestType'] == "SaveFormTemplate":
        print("Saving form template")
        return forms.saveFormTemplate(requestData['Data'])
    elif requestData['RequestType'] == "GetFormTemplateList":
        print("Getting form template list")
        return forms.getFormTemplateList(requestData['Data'])
    elif requestData['RequestType'] == "GetFormTemplateData":
        print("Getting form template data")
        return forms.getFormTemplateData(requestData['Data'])
    elif requestData['RequestType'] == "CreateFormSubmission":
        print("creating form submission")
        return forms.createFormSubmission(requestData['Data'])
    elif requestData['RequestType'] == "GetFormSubmissionData":
        print("getting form submission data")
        return forms.getFormSubmissionData(requestData['Data'])
    elif requestData['RequestType'] == "SaveFormSubmission":
        print("getting form submission data")
        return forms.saveFormSubmission(requestData['Data'])
    elif requestData['RequestType'] == "SubmitFormSubmission":
        print("submitted form")
        return forms.submitFormSubmission(requestData['Data'])
    elif requestData['RequestType'] == "GetMyForms":
        print("getting my forms")
        return forms.getMyForms(requestData['Data'])
    elif requestData['RequestType'] == "GetPendingForms":
        print("getting pending forms")
        return forms.getPendingForms(requestData['Data'])
    elif requestData['RequestType'] == "CompleteFormReview":
        print("Completing Form Review")
        return forms.completeFormReview(requestData['Data'])
    elif requestData['RequestType'] == "GetFormTemplateHistory":
        print("Get Form Template History")
        return forms.getFormTemplateHistory(requestData['Data'])
    elif requestData['RequestType'] == "DeleteFormSubmission":
        return forms.deleteFormSubmission(requestData['Data'])
    elif requestData['RequestType'] == "DeleteFormTemplate":
        return forms.deleteFormTemplate(requestData['Data'])

    ##########################################################################

    elif requestData['RequestType'] == "CheckUserProfileAccountability":
        print("Add users to role")
        # everything else in here don't touch
        return checkPermssionForProfileAccountability(requestData['Data'])

    ###########################################################################################

    ############################Waste Function Routing#####################################
    elif requestData['RequestType'] == "SaveCustomProduct":
        return waste.saveCustomProduct(requestData['Data'])
    elif requestData['RequestType'] == "DeleteCustomProduct":
        return waste.deleteCustomProduct(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteReportingData":
        return waste.getWasteReportingData(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteReportingDayPartData":
        return waste.getWasteReportingDayPartData(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteOverTime":
        return waste.getWasteOverTime(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteReportingMonthyCalendarData":
        return waste.getWasteReportingMonthlyCalendarData(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteReportingWeeklyCalendarData":
        return waste.getWasteReportingWeeklyCalendarData(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteReportingDailyWaste":
        return waste.getWasteReportingDailyWaste(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteCategories":
        return waste.getWasteCategories(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteReportingReasonData":
        return waste.getWasteReportingWasteByReason(requestData['Data'])
    elif requestData['RequestType'] == "GetProductByReasonData":
        return waste.getWasteProductsByReason(requestData['Data'])
    elif requestData['RequestType'] == "GetProductByReasonAndDate":
        return waste.getWasteProductsByReasonAndDate(requestData['Data'])
    elif requestData['RequestType'] == "GetProductByReasonAndMinute":
        return waste.getWasteProductsByReasonAndMinute(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteLogInstance":
        return waste.getWasteLogInstance(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteProductsReport":
        print("getting products report")
        return waste.getWasteProductsReport(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteDaypartsReport":
        print("getting daypart report")
        return waste.getWasteDaypartsReport(requestData['Data'])
    elif requestData['RequestType'] == "GetWasteInteractionsReport":
        print("getting daypart report")
        return waste.getWasteInteractionsReport(requestData['Data'])

    elif requestData['RequestType'] == "GetAPIUsers":  # VendorBridgeAPI
        return vendorBridgeAPI.getAPIUsers(requestData['Data'])
    elif requestData['RequestType'] == "RunUserAPI":
        return vendorBridgeAPI.runUserAPI(requestData['Data'])
    elif requestData['RequestType'] == "SendUserInvites":
        return vendorBridgeAPI.sendUserInvites(requestData['Data'])

    ########################Accountability Reporting Routing#############################
    elif requestData['RequestType'] == "GetAccountabilityReportingHomeData":
        return accountabilityReportingHome.getAccountabilityReportingHomeData(requestData['Data'])
    elif requestData['RequestType'] == "GetAccountabilityReportingHomeInfractionsByDayData":
        return accountabilityReportingHome.getAccountabilityHomeInfractionsByDay(requestData['Data'])
    elif requestData['RequestType'] == "GetAccountabilityReportingHomeInfractionsByRoleData":
        return accountabilityReportingHome.getAccountabilityHomeInfractionsByRole(requestData['Data'])
    elif requestData['RequestType'] == "GetUserAccountabilityLog":
        return accountabilityReportingHome.getUserAccountabilityLog(requestData['Data'])
    elif requestData['RequestType'] == "GetAccountabilityReportingHomeInfractionsByDayBottomSheetData":
        return accountabilityReportingInfractionsByDay.getInfractionsByDayBottomSheetData(requestData['Data'])
    elif requestData['RequestType'] == "GetAccountabilityReportingHomeInfractionsByRoleBottomSheetData":
        return accountabilityReportingInfractionsByDay.getInfractionsByRoleBottomSheetData(requestData['Data'])
    elif requestData['RequestType'] == "GetTotalAccountabilityInfractions":
        return accountabilityReportingTotalAccountability.getTotalAccountabilityInfractions(requestData['Data'])
    elif requestData['RequestType'] == "GetTotalAccountabilityDAs":
        return accountabilityReportingTotalAccountability.getTotalAccountabilityDisciplinaryActions(requestData['Data'])
    elif requestData['RequestType'] == "GetInfractionsByWeek":
        return accountabilityReportingInfractionsByWeek.getInfractionsByWeekSummary(requestData['Data'])
    elif requestData['RequestType'] == "GetWeeklyInfractionsProduct":
        return accountabilityReportingInfractionsByWeek.getWeekInfractionsProduct(requestData['Data'])
    elif requestData['RequestType'] == "GetWeeklyInfractionsUser":
        return accountabilityReportingInfractionsByWeek.getWeekInfractionsUsers(requestData['Data'])
    elif requestData['RequestType'] == "GetDayRoleInfractionsUser":
        return accountabilityReportingInfractionsByDay.getInfractionsByDayInstances(requestData['Data'])

    #########################################################################################################

    ###########################Dashboard To-DO Function Routing####################################################
    elif requestData['RequestType'] == "GetDashboardToDoListScreenData":
        print('getting todays to dos')
        print(requestData)
        return dashboardToDoList.getDashboardToDoList(requestData['Data'])
    elif requestData['RequestType'] == "GetDashboardUpcomingToDos":
        print('getting upcoming todos')
        return dashboardToDoList.getDashboardUpcomingToDos(requestData['Data'])

    #########################################################################################################

    ###########################Dashboard Task Function Routing####################################################
    elif requestData['RequestType'] == "GetDashboardTaskScreen":
        return dashboardTasks.getDashboardTaskScreen(requestData['Data'])
    #########################################################################################################

    ###########################Dashboard Points Function Routing####################################################
    elif requestData['RequestType'] == "GetMyClaimedRewards":
        return dashboardPoints.getMyClaimedRewards(requestData['Data'])
    elif requestData['RequestType'] == "GetMyPointsHistory":
        return dashboardPoints.getMyPointsHistory(requestData['Data'])
#########################################################################################################

    ###########################Dashboard Checkin Function Routing####################################################
    elif requestData['RequestType'] == "GetDashboardCheckInData":

        return dashboardCheckin.getDashboardCheckinData(requestData['Data'])
    elif requestData['RequestType'] == "GetDashboardCheckinUpcomingData":

        return dashboardCheckin.getDashboardUpcomingCheckinData(requestData['Data'])

    else:
        response = {
            "Data": "None", "Error": "Sorry, that request doesn't exist.  Please contact your system administrator"}
        print(response)
        return json.dumps(response)


def sanitizeText(text):
    delimitingCharacter = "\\"
    removeCharacter = text.replace('\'', f'{delimitingCharacter}\'')
    newText = removeCharacter.replace('"', f'{delimitingCharacter}"')
    return newText


def getQuarterParameters(date):

    dateObject = datetime.datetime.fromisoformat(str(date))

    startDate = ''
    endDate = ''
    if(dateObject.month >= 1 and dateObject.month <= 3):
        startDate = f'{dateObject.year}-01-01'
        endDate = f'{dateObject.year}-03-31'
    elif (dateObject.month >= 4 and dateObject.month <= 6):
        startDate = f'{dateObject.year}-04-01'
        endDate = f'{dateObject.year}-06-30'
    elif (dateObject.month >= 7 and dateObject.month <= 9):
        startDate = f'{dateObject.year}-07-01'
        endDate = f'{dateObject.year}-09-30'
    elif (dateObject.month >= 10 and dateObject.month <= 12):
        startDate = f'{dateObject.year}-10-01'
        endDate = f'{dateObject.year}-12-31'

    return startDate, endDate


# THESE ARE VSBL FUNCTIONS TO BE ALTERED AND MODIFIED LATER


# NOTIFICATION RELATED THINGS

def sendPushNotification(userID, title, body, payload):
    try:
        db = mysql.connector.connect(
            host=accountsEndpoint,
            user='admin',
            passwd='adminpass',
            database='Accounts'
        )
        print('Connected!')
        cursor = db.cursor()

    except:
        print("Couldn't connect to database")
        response = {
            "Data": "None", "Error": "Couldn't connect to database.  Try again or contact your administrator"}
        return json.dumps(response)

    try:
        serverToken = 'AAAA7iJcuMI:APA91bHr_H8f-mH4gdHvnlP02zLNL0kFIQ4Aj8kM-aH7zVszoqJ3xyfupQUT33dwzjq0fht5AcvuxnUe9BmfQ-xD79d_Cegxyjd74iYiq4oTPMjF8IcpYHOG81hgBmP43jeoz881522T'

        cursor.execute(
            f"select PushNotificationToken from Users where UserID = {userID}")
        results = cursor.fetchall()
        token = results[0][0]

        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + serverToken,
        }
        if(payload != None):
            body = {
                'notification': {'title': f'{title}',
                                 'body': f'{body}',

                                 },
                'to':
                token,
                'data': payload,
                'priority': 'high',
            }
        else:
            body = {
                'notification': {'title': f'{title}',
                                 'body': f'{body}',

                                 },
                'to':
                token,
                'data': {"Type": "Push"},
                'priority': 'high',
            }

        response = requests.post(
            "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
        print(response.status_code)

        return 1

    except:
        return 0


def getDashboardToDoList(data):
    try:
        db = mysql.connector.connect(
            host=data["DatabaseEndpoint"],
            user='admin',
            passwd='adminpass',
            database=data["Database"]
        )
        print('Connected!')
        cursor = db.cursor()

    except:
        print("Couldn't connect to database")
        response = {
            "Data": "None", "Error": "Couldn't connect to database.  Try again or contact your administrator"}
        return json.dumps(response)

    try:
        cursor.execute(
            "SET @@session.time_zone = '{}'".format(data["TimeZone"]))
    except:
        print("Couldn't set time zone")
        response = {
            "Data": "None", "Error": "Couldn't set timezone for data collection.  Try again or contact your administrator"}
        return json.dumps(response)

    try:
        print(data)
        userID = data["UserID"]
        date = data["Date"]
        toDotype = data["ToDoTypeID"]
        completed = data["Completed"]
        pageIndex = data["PageIndex"]
        offset = 15 * pageIndex
        if(data["Person"] != "Myself"):
            query = f"select * from (select *, (select FirstName from Users where UserID = tdl.AssignedTo) as FirstName, (select LastName from Users where UserID = tdl.AssignedTo) as LastName from ToDoLog tdl left join (select ChecklistSubmissionID, ChecklistSubmissionContent from ChecklistSubmission) cl on (cl.ChecklistSubmissionID = tdl.ForeignObjectID) left join (select * from SafeCounts) sc on sc.SafeCountID = tdl.ForeignObjectID where (date(DueDate) = '{date}' ||  (date(DueDate) < '{date}' and ToDoTypeID = 1 and tdl.Completed = 0)) and AssignedTo like '{userID}' and ToDoTypeID like '{toDotype}' and ToDoTypeID not in (3,4,5,6,7,8,9) and Completed like '{completed}' order by tdl.Completed asc) as dataSet limit 15 offset {offset};"

        else:
            query = f"select * from (select *, (select FirstName from Users where UserID = tdl.AssignedTo) as FirstName, (select LastName from Users where UserID = tdl.AssignedTo) as LastName from ToDoLog tdl left join (select ChecklistSubmissionID, ChecklistSubmissionContent from ChecklistSubmission) cl on (cl.ChecklistSubmissionID = tdl.ForeignObjectID) left join (select * from SafeCounts) sc on sc.SafeCountID = tdl.ForeignObjectID where (date(DueDate) = '{date}' ||  (date(DueDate) < '{date}' and ToDoTypeID = 1 and tdl.Completed = 0)  || (tdl.ToDoTypeID = 7 and tdl.Completed = 0) || (ToDoTypeID = 6 and tdl.Completed = 0) || (ToDoTypeID = 8 and tdl.Completed = 0) || (ToDoTypeID = 9 and tdl.Completed = 0)) and AssignedTo like '{userID}' and ToDoTypeID like '{toDotype}' and Completed like '{completed}' order by tdl.Completed asc) as dataSet limit 15 offset {offset};"
            print(query)
        cursor.execute(query)
        results = cursor.fetchall()
        row_headers = [x[0] for x in cursor.description]
        mappedData = []
        for i in results:
            mappedData.append(dict(zip(row_headers, i)))

        response = {
            "Data": mappedData, "Error": "None"}

        return json.dumps(response, default=defaultconverter)

    except:
        response = {"Data": "None", "Error": "Couldn't save image"}
        return json.dumps(response)


def getChecklistDashboardList(data):
    try:
        db = mysql.connector.connect(
            host=data["DatabaseEndpoint"],
            user='admin',
            passwd='adminpass',
            database=data["Database"]
        )
        print('Connected!')
        cursor = db.cursor()

    except:
        print("Couldn't connect to database")
        response = {
            "Data": "None", "Error": "Couldn't connect to database.  Try again or contact your administrator"}
        return json.dumps(response)

    try:
        cursor.execute(
            "SET @@session.time_zone = '{}'".format(data["TimeZone"]))
    except:
        print("Couldn't set time zone")
        response = {
            "Data": "None", "Error": "Couldn't set timezone for data collection.  Try again or contact your administrator"}
        return json.dumps(response)

    try:
        userID = data["UserID"]
        date = data["Date"]
        checklistType = data["ChecklistTypeID"]
        completed = data["Completed"]
        query = f"select (select ChecklistTemplateName from ChecklistTemplate where ChecklistTemplateID = cs.ChecklistTemplateID) as ChecklistTemplateName, cs.ChecklistSubmissionID, cs.DueDate, cs.Started, cs.CompletedFields, (select TotalFields from ChecklistTemplate where ChecklistTemplateID = cs.ChecklistTemplateID) as TotalFields, cs.Completed, (select concat(concat(FirstName, ' '), LastName) from Users where UserID in (select AssignedTo from ToDoLog where ToDoTypeID = 2 and ForeignObjectID = cs.ChecklistSubmissionID)) as Owner, (select AssignedTo from ToDoLog where ToDoTypeID = 2 and ForeignObjectID = cs.ChecklistSubmissionID) as UserID, cs.ChecklistSubmissionContent from ChecklistSubmission cs where cs.ChecklistTemplateID in (select ChecklistTemplateID from ChecklistTemplate where TeamTypeID like '%') and ChecklistSubmissionID in (select ForeignObjectID from ToDoLog where ToDoTypeID = 2 and AssignedTo like '{userID}') and cs.Completed like '{completed}' and cs.ChecklistTemplateID in (select ChecklistTemplateID from ChecklistTemplate where ChecklistTypeID like '{checklistType}') and date(DueDate) = '{date}';"
        print(query)
        cursor.execute(query)
        results = cursor.fetchall()
        row_headers = [x[0] for x in cursor.description]
        mappedData = []
        for i in results:
            mappedData.append(dict(zip(row_headers, i)))

        response = {
            "Data": mappedData, "Error": "None"}
        return json.dumps(response, default=defaultconverter)

    except:
        response = {"Data": "None", "Error": "Couldn't save image"}
        return json.dumps(response)


def checkPermssionForProfileAccountability(data):
    try:
        db = mysql.connector.connect(
            host=data["DatabaseEndpoint"],
            user='admin',
            passwd='adminpass',
            database=data["Database"]
        )
        print('Connected!')
        cursor = db.cursor()

    except:
        print("Couldn't connect to database")
        response = {
            "Data": "None", "Error": "Couldn't connect to database.  Try again or contact your administrator"}
        return json.dumps(response)

    try:
        localUserID = data["LocalUserID"]
        passedUserID = data["PassedUserID"]

        query = f"select(case when ((select UserID from UserPermissions where UserID = {localUserID} and PermissionTypeID = 14) or (select RoleID from RolePermissions where RoleID in(select RoleID from UserRoles where UserID = {localUserID}) and PermissionTypeID = 14)) and (select RoleID from Roles where (HierarchyIndex < (select HierarchyIndex from Roles where RoleID in (select RoleID from UserRoles where UserID = {passedUserID}))) and RoleID in (select RoleID from UserRoles where UserID = {localUserID})) then 1 else 0 end) from dual;"
        cursor.execute(query)
        results = cursor.fetchall()

        response = {
            "Data": results[0][0], "Error": "None"}
        return json.dumps(response, default=defaultconverter)

    except:
        response = {"Data": "None", "Error": "Couldn't update permission"}
        return json.dumps(response)


def getLeaderBoard(data):
    try:
        db = mysql.connector.connect(
            host=data["DatabaseEndpoint"],
            user='admin',
            passwd='adminpass',
            database=data["Database"]
        )
        print('Connected!')
        cursor = db.cursor()

    except:
        print("Couldn't connect to database")
        response = {
            "Data": "None", "Error": "Couldn't connect to database.  Try again or contact your administrator"}
        return json.dumps(response)

    try:
        cursor.execute(
            "SET @@session.time_zone = '{}'".format(data["TimeZone"]))
    except:
        print("Couldn't set time zone")
        response = {
            "Data": "None", "Error": "Couldn't set timezone for data collection.  Try again or contact your administrator"}
        return json.dumps(response)

    try:

        query = f"""select distinct UserID, sum(PointAmount) as Points, (select FirstName from Users where UserID = pl.UserID) as FirstName, 
        (select LastName from Users where UserID = pl.UserID) as LastName from PointLog pl 
        where PointAmount > 0 and Date(CreationDate) >= '2022-07-01' and Date(CreationDate) <= '2022-07-14' group by pl.UserID order by Points desc;"""
        cursor.execute(query)
        results = cursor.fetchall()

        mappedData = []
        row_headers = [x[0] for x in cursor.description]

        for i in results:
            mappedData.append(dict(zip(row_headers, i)))

        response = {
            "Data": mappedData, "Error": "None"}

        return json.dumps(response, default=str)

    except:
        response = {"Data": "None",
                    "Error": "Unable to retrieve contest data"}
        return json.dumps(response)
