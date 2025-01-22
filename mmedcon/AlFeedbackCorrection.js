import wixData from 'wix-data';
import wixUsers from 'wix-users';


class FeedbackManager {
    constructor() {
        this.currentUser = wixUsers.currentUser;
        this.currentUserEmail = null;
    }


    async init() {
        this.hideAllSections();

        try {
            if (!this.currentUser.loggedIn) {
                $w("#verifyUserError").text = "You must be logged in to access this page.";
                $w("#verifyUserError").show();
                return; // Stop further execution if the user is not logged in
           }

            this.currentUserEmail = await this.currentUser.getEmail();
            
            await this.verifyGrader(); // Verify if the user is a grader
            await this.populateRoundDropdown();

            // Event Handlers
            $w("#roundDropdown").onChange(() => this.onRoundChange());
            $w("#caseStudyDropdown").onChange(() => this.onCaseStudyChange());
            $w("#submissionDropdown").onChange(() => this.onUserChange());
            $w("#answerTypeDropdown").onChange(() => this.onAnswerTypeChange());
            $w("#modificationCheckbox").onChange(() => this.onModificationChange());
            $w("#saveButton").onClick(() => this.onSave());
        } catch (error) {
            this.showError("An error occurred during initialization. Please try again later.");
        }
    }

     async verifyGrader() {
       const userQuery = await wixData.query("userInfo").eq("emailAddress", this.currentUserEmail).find();


       if (userQuery.items.length === 0 || userQuery.items[0].userType !== 'grader') {
           $w("#verifyUserError").text = "Access denied. Only graders are allowed to review feedback.";
           $w("#verifyUserError").show();
           throw new Error("Unauthorized access attempt.");
       }
   }

    hideAllSections() {
        ["#caseStudyDropdown", "#submissionDropdown", "#answerTypeDropdown", "#studentAnswerText", "#feedbackText", 
         "#gradingRubricText", "#scoreValue", "#modificationCheckbox", 
         "#feedbackInput", "#scoreInput", "#gradingRubricInput", "#saveButton", 
         "#errorMessage", "#successMessage"].forEach(id => $w(id).hide());
    }

    showError(message) {
        $w("#errorMessage").text = message;
        $w("#errorMessage").show();
    }

    showSuccess(message) {
        $w("#successMessage").text = message;
        $w("#successMessage").show();
    }

    async populateRoundDropdown() {
        try {
            const results = await wixData.query("roundInfo").ascending("roundNum").find();
            if (results.items.length === 0) {
                this.showError("No rounds available.");
                return;
            }

            const roundOptions = results.items.map(item => ({
                label: `Round ${item.roundNum}`,
                value: item.roundNum
            }));

            $w("#roundDropdown").options = roundOptions;
        } catch (error) {
            this.showError("Error loading rounds. Please try again.");
        }
    }

    async onRoundChange() {
        $w("#text83").hide(); // Hide error message
        const selectedRound = $w("#roundDropdown").value;
        if (!selectedRound) {
            this.showError("Please select a valid round.");
            return;
        }

        await this.populateCaseStudyDropdown(selectedRound);
    }

    async populateCaseStudyDropdown(selectedRound) {
    try {
        // Step 1: Query the roundInfo collection
        const roundResults = await wixData.query("roundInfo")
            .eq("roundNum", selectedRound) // Match selected round
            .find();

        if (roundResults.items.length === 0) {
            this.showError("No matching round found.");
            return;
        }

        const roundId = roundResults.items[0]._id;

        // Step 2: Query the CaseStudies collection
        const caseStudyResults = await wixData.query("CaseStudies")
            .eq("roundNum", roundId) // Match round ID in case studies
            .find();

        if (caseStudyResults.items.length === 0) {
            this.showError("No case studies found for the selected round.");
            return;
        }

        // Step 3: Map the case study data to dropdown options
        const caseStudyOptions = caseStudyResults.items.map(item => ({
            label: item.caseStudyName, // Display name
            value: item._id // Value for dropdown
        }));

        // Step 4: Populate the case study dropdown
        $w("#caseStudyDropdown").options = caseStudyOptions;
        $w("#caseStudyDropdown").show();

    } catch (error) {
        this.showError("Error loading case studies. Please try again.");
    }
}

    async onCaseStudyChange() {

        $w("#text83").hide(); // Hide error message
        $w("#submissionDropdown").options = [];
        $w("#submissionDropdown").hide();
        $w("#answerTypeDropdown").hide();
        this.clearFeedbackSection();

        const selectedCaseStudy = $w("#caseStudyDropdown").value;
        if (!selectedCaseStudy) {
            this.showError("Please select a valid case study.");
            return;
        }

        await this.populateSubmissionDropdown(selectedCaseStudy);
    }

    async populateSubmissionDropdown(caseStudyID) {
    try {
        // Clear and hide the dropdown initially
        $w("#submissionDropdown").options = [];
        $w("#submissionDropdown").hide();

        // Query submissions for the selected case study
        const submissionsQuery = await wixData.query("submissions")
            .eq("caseStudyID", caseStudyID)
            .find();

        if (submissionsQuery.items.length === 0) {
            $w("#text83").text = "No submissions found for the selected case study.";
            $w("#text83").show();
            return;
        }

        const submissionIDs = submissionsQuery.items.map(item => item._id);

        // Query feedbackTable to find ungraded submissions
        const feedbackQuery = await wixData.query("feedbackTable")
            .hasSome("submissionID", submissionIDs)
            .eq("gradedStatus", false) // Filter for ungraded feedback
            .find();

        if (feedbackQuery.items.length === 0) {
            $w("#text83").text = "No ungraded submissions found for the selected case study.";
            $w("#text83").show()            
            return;
        }

        // Map ungraded feedback to submission IDs
        const userOptions = feedbackQuery.items
            .filter(feedback => feedback.submissionID && feedback.submissionID !== "")
            .map(feedback => ({
                label: `${feedback.submissionID}`,
                value: feedback.submissionID
            }));


        if (userOptions.length === 0) {
            this.showError("No valid submissions found.");
            return;
        }

        // Populate the user dropdown
        $w("#submissionDropdown").options = userOptions;
        $w("#submissionDropdown").show();

    } catch (error) {
        this.showError("Error loading submissions. Please try again.");
    }
}

    async onUserChange() {
    // Reset feedback-related UI elements
    this.clearFeedbackSection();

    const selectedSubmissionID = $w("#submissionDropdown").value;
    const caseStudyID = $w("#caseStudyDropdown").value;

    if (!selectedSubmissionID || !caseStudyID) {
        this.showError("Please select a valid submission and case study.");
        return;
    }

    // Use the submissionID for further actions instead of studentID
    await this.populateAnswerTypeDropdown(selectedSubmissionID);
}


   async populateAnswerTypeDropdown(submissionID) {
    try {
        if (!submissionID) {
            this.showError("No submission selected to populate answer types.");
            return;
        }

        // Step 1: Retrieve the feedback entry for the given submissionID
        const feedbackQuery = await wixData.query("feedbackTable")
            .eq("submissionID", submissionID)
            .find();

        if (feedbackQuery.items.length === 0) {
            this.showError("No feedback entry found for the selected submission.");
            return;
        }

        const feedback = feedbackQuery.items[0];

        // Step 2: Get the list of reviewed questions
        const questionsReviewed = feedback.questionsReviewed || [];

        // Step 3: Define all possible question types
        const allQuestions = [
            { label: "Differential Diagnosis", value: "differentialDiagnosis" },
            { label: "Selected Diagnosis", value: "selectedDiagnosis" },
            { label: "Treatment", value: "treatment" },
            { label: "Clinical Tests", value: "clinicalTests" }
        ];

        // Step 4: Filter out the reviewed questions
        const availableQuestions = allQuestions.filter(
            (question) => !questionsReviewed.includes(question.value)
        );

        // Step 5: Update the dropdown options
        if (availableQuestions.length === 0) {
            this.showError("All questions have already been reviewed for this submission.");
            $w("#answerTypeDropdown").hide();
            return;
        }

        $w("#answerTypeDropdown").options = availableQuestions;
        $w("#answerTypeDropdown").show();

    } catch (error) {
        this.showError("Error populating answer type dropdown. Please try again.");
    }
}


async onAnswerTypeChange() {
    // Clear feedback-related UI elements
    this.clearFeedbackSection();

    const selectedAnswerType = $w("#answerTypeDropdown").value;
    const selectedSubmissionID = $w("#submissionDropdown").value;
    const caseStudyID = $w("#caseStudyDropdown").value;

    if (!selectedAnswerType || !selectedSubmissionID || !caseStudyID) {
        this.showError("Please select a valid answer type, submission, and case study.");
        return;
    }

    // Display feedback for the selected case study, submission, and answer type
    await this.displayFeedback(caseStudyID, selectedSubmissionID, selectedAnswerType);
}

    async displayFeedback(caseStudyID, submissionID, answerType) {
    try {
        // Step 1: Retrieve Submission Details
        const submissionQuery = await wixData.query("submissions")
            .eq("_id", submissionID)
            .find();

        if (submissionQuery.items.length === 0) {
            this.showError("No submission found for the selected ID.");
            return;
        }

        const submission = submissionQuery.items[0];

        // Step 2: Retrieve Feedback Details
        const feedbackQuery = await wixData.query("feedbackTable")
        .eq("submissionID", submissionID) // Match the reference
        .include("submissionID") // Include referenced submission data
        .find();

        if (feedbackQuery.items.length === 0) {
            return;
        }

        const feedback = feedbackQuery.items[0];
        const submissionData = feedback.submissionID; // This now contains the referenced submission data

        // Step 3: Retrieve Grading Rubric
        const rubricQuery = await wixData.query("gradingRubrics")
            .eq("caseStudyId", caseStudyID)
            .find();

        if (rubricQuery.items.length === 0) {
            this.showError("No grading rubric available for the selected case study.");
            return;
        }

        const gradingRubric = rubricQuery.items[0];

        // Step 4: Display the Student Answer
        let studentAnswer = "No answer provided.";
        switch (answerType) {
            case "differentialDiagnosis":
                studentAnswer = submission.differentialDiagnosis || studentAnswer;
                break;
            case "selectedDiagnosis":
                studentAnswer = submission.selectedDiagnosis || studentAnswer;
                break;
            case "treatment":
                studentAnswer = submission.treatment || studentAnswer;
                break;
            case "clinicalTests":
                studentAnswer = submission.clinicalTests || studentAnswer;
                break;
            default:
                studentAnswer = "Unknown question type.";
        }

        // Step 5: Display the Feedback and Score
        let questionFeedback = "No feedback provided.";
        let questionScore = "No score available.";
        switch (answerType) {
            case "differentialDiagnosis":
                questionFeedback = feedback.feedbackDd || questionFeedback;
                questionScore = feedback.scoreDd !== undefined ? feedback.scoreDd : questionScore;
                break;
            case "selectedDiagnosis":
                questionFeedback = feedback.feedbackSd || questionFeedback;
                questionScore = feedback.scoreSd !== undefined ? feedback.scoreSd : questionScore;
                break;
            case "treatment":
                questionFeedback = feedback.feedbackT || questionFeedback;
                questionScore = feedback.scoreT !== undefined ? feedback.scoreT : questionScore;
                break;
            case "clinicalTests":
                questionFeedback = feedback.feedbackCt || questionFeedback;
                questionScore = feedback.scoreCt !== undefined ? feedback.scoreCt : questionScore;
                break;
            default:
                questionFeedback = "No feedback available.";
                questionScore = "No score available.";
        }

        // Step 6: Update the UI
        $w("#studentAnswerText").text = studentAnswer;
        $w("#feedbackText").text = questionFeedback;
        $w("#gradingRubricText").text = gradingRubric[answerType] || "No rubric available.";
        $w("#scoreValue").text = `${questionScore}`;

        // Step 7: Show Relevant Sections
        $w('#box1').show();
        $w('#box2').show();
        $w('#box5').show();
        $w('#box4').show();
        $w('#text76').show();
        $w('#text77').show();
        $w('#text82').show();
        $w('#text80').show();
        $w("#studentAnswerText").show();
        $w("#feedbackText").show();
        $w("#gradingRubricText").show();
        $w("#scoreValue").show();
        $w("#modificationCheckbox").show();
    } catch (error) {
        this.showError("Error displaying feedback. Please try again.");
    }
}


    async onModificationChange() {
        const selectedOptions = $w("#modificationCheckbox").value;
        $w("#feedbackInput").hide();
        $w("#scoreInput").hide();
        $w("#gradingRubricInput").hide();

        if (selectedOptions.includes("editFeedback")) $w("#feedbackInput").show();
        if (selectedOptions.includes("editScore")) $w("#scoreInput").show();
        if (selectedOptions.includes("editGradingRubric")) $w("#gradingRubricInput").show();

        $w("#saveButton").show();
    }

async onSave() {
    // Retrieve data from the UI
    const selectedAnswerType = $w("#answerTypeDropdown").value;
    const caseStudyID = $w("#caseStudyDropdown").value;
    const selectedSubmissionID = $w("#submissionDropdown").value;
    const feedbackInput = $w("#feedbackInput").value;
    const scoreInput = parseFloat($w("#scoreInput").value);
    const gradingRubricInput = $w("#gradingRubricInput").value;

    try {
        // Step 1: Fetch feedback entry
        const feedbackQuery = await wixData.query("feedbackTable")
            .eq("submissionID", selectedSubmissionID)
            .include("studentId") // Ensure studentId is expanded
            .find();

        if (feedbackQuery.items.length === 0) {
            this.showError("No feedback entry found to update.");
            return;
        }

        const feedbackToUpdate = feedbackQuery.items[0];

        // Check if studentId is expanded properly
        if (!feedbackToUpdate.studentId?._id) {
            this.showError("Failed to retrieve student details.");
            return;
        }

        const studentId = feedbackToUpdate.studentId._id;

        // Step 2: Update feedback if provided
        if (feedbackInput) {
            switch (selectedAnswerType) {
                case "differentialDiagnosis":
                    feedbackToUpdate.feedbackDd = feedbackInput;
                    break;
                case "selectedDiagnosis":
                    feedbackToUpdate.feedbackSd = feedbackInput;
                    break;
                case "treatment":
                    feedbackToUpdate.feedbackT = feedbackInput;
                    break;
                case "clinicalTests":
                    feedbackToUpdate.feedbackCt = feedbackInput;
                    break;
                default:
                    this.showError("Invalid question type for feedback update.");
                    return;
            }
        }

        // Step 3: Update score if provided and valid
        if (!isNaN(scoreInput)) {
            switch (selectedAnswerType) {
                case "differentialDiagnosis":
                    feedbackToUpdate.scoreDd = scoreInput;
                    break;
                case "selectedDiagnosis":
                    feedbackToUpdate.scoreSd = scoreInput;
                    break;
                case "treatment":
                    feedbackToUpdate.scoreT = scoreInput;
                    break;
                case "clinicalTests":
                    feedbackToUpdate.scoreCt = scoreInput;
                    break;
                default:
                    this.showError("Invalid question type for score update.");
                    return;
            }

            // Recalculate the total score
            feedbackToUpdate.score = (feedbackToUpdate.scoreDd || 0) +
                                     (feedbackToUpdate.scoreSd || 0) +
                                     (feedbackToUpdate.scoreT || 0) +
                                     (feedbackToUpdate.scoreCt || 0);
        }

        // Step 4: Mark feedback as graded
        if (!feedbackToUpdate.questionsReviewed) {
            feedbackToUpdate.questionsReviewed = [];
        }
        if (!feedbackToUpdate.questionsReviewed.includes(selectedAnswerType)) {
            feedbackToUpdate.questionsReviewed.push(selectedAnswerType);
        }

        // Check if all questions have been reviewed
        const allQuestions = ["differentialDiagnosis", "selectedDiagnosis", "treatment", "clinicalTests"];
        feedbackToUpdate.gradedStatus = allQuestions.every(question =>
            feedbackToUpdate.questionsReviewed.includes(question)
        );

        await wixData.update("feedbackTable", feedbackToUpdate);

        // Step 5: Update the grading rubric if provided
        if (gradingRubricInput) {
            const rubricQuery = await wixData.query("gradingRubrics")
                .eq("caseStudyId", caseStudyID)
                .find();

            if (rubricQuery.items.length > 0) {
                const rubricToUpdate = rubricQuery.items[0];
                rubricToUpdate[selectedAnswerType] = gradingRubricInput;

                await wixData.update("gradingRubrics", rubricToUpdate);
            } else {
                return;
            }
        }

        // Step 6: Display success message
        this.showSuccess("Updated successfully.");

        // Step 8: Refresh feedback
        await this.displayFeedback(caseStudyID, selectedSubmissionID, selectedAnswerType);

        // Reset the page after 5 seconds
        setTimeout(() => this.resetPage(), 5000);
    } catch (error) {
        this.showError("Error saving changes. Please try again.");
    }
}

clearFeedbackSection() {
    // Clear text elements
    $w("#studentAnswerText").text = "";
    $w("#feedbackText").text = "";
    $w("#gradingRubricText").text = "";
    $w("#scoreValue").text = "";

    // Hide text and input elements
    ["#studentAnswerText", "#feedbackText", "#gradingRubricText", "#scoreValue", 
     "#modificationCheckbox", "#feedbackInput", "#scoreInput", "#gradingRubricInput", 
     "#saveButton"].forEach(id => $w(id).hide());
}

resetPage() {

    // Clear dropdown values
    $w("#roundDropdown").value = null;
    $w("#caseStudyDropdown").value = null;
    $w("#submissionDropdown").value = null;
    $w("#answerTypeDropdown").value = null;

    // Clear dropdown options
    $w("#caseStudyDropdown").options = [];
    $w("#submissionDropdown").options = [];
    $w("#answerTypeDropdown").options = [];

    // Explicitly hide modification checkbox
    $w("#modificationCheckbox").value = []; // Reset its values
    $w("#modificationCheckbox").hide();

    // Hide dropdowns
    ["#caseStudyDropdown", "#submissionDropdown", "#answerTypeDropdown"].forEach(id => $w(id).hide());

    // Clear text fields
    $w("#studentAnswerText").text = "";
    $w("#feedbackText").text = "";
    $w("#gradingRubricText").text = "";
    $w("#scoreValue").text = "";

    // Hide text and input fields
    [
        "#text83",
        "#verifyUserError",
        "#studentAnswerText",
        "#feedbackText",
        "#gradingRubricText",
        "#scoreValue",
        "#feedbackInput",
        "#scoreInput",
        "#gradingRubricInput",
        "#saveButton"
    ].forEach(id => $w(id).hide());

    // Clear and hide success and error messages
    $w("#successMessage").text = "";
    $w("#successMessage").hide();
    $w("#errorMessage").text = "";
    $w("#errorMessage").hide();
}


}

// Initialize the class
$w.onReady(() => {
    const feedbackManager = new FeedbackManager();
    feedbackManager.init();
});
