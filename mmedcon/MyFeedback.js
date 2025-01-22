import wixData from 'wix-data';
import wixUsers from 'wix-users';

class Feedback {
    constructor(feedbackData) {
        this.feedbackT = feedbackData.feedbackT || "No feedback available";
        this.scoreT = feedbackData.scoreT !== undefined ? `${feedbackData.scoreT}` : "Score: N/A";

        this.feedbackDd = feedbackData.feedbackDd || "No feedback available";
        this.scoreDd = feedbackData.scoreDd !== undefined ? `${feedbackData.scoreDd}` : "Score: N/A";

        this.feedbackSd = feedbackData.feedbackSd || "No feedback available";
        this.scoreSd = feedbackData.scoreSd !== undefined ? `${feedbackData.scoreSd}` : "Score: N/A";

        this.feedbackCt = feedbackData.feedbackCt || "No feedback available";
        this.scoreCt = feedbackData.scoreCt !== undefined ? `${feedbackData.scoreCt}` : "Score: N/A";

        this.totalScore = feedbackData.score !== undefined ? `${feedbackData.score}` : "Score: N/A";
    }

    static fromWixData(feedbackData) {
        return new Feedback(feedbackData);
    }
}

class FeedbackDisplayManager {
    constructor() {
        this.currentUser = wixUsers.currentUser;
        this.currentUserEmail = null;
    }

    async init() {
        try {
            if (!this.currentUser.loggedIn) {
                this.showError("You must be logged in to view your feedback.");
                return;
            }

            this.currentUserEmail = await this.currentUser.getEmail();
            if (!this.currentUserEmail) {
                this.showError("Error retrieving your email. Please log in again.");
                return;
            }

            // Verify if the user is a student
            const userQuery = await wixData.query("userInfo")
                .eq("emailAddress", this.currentUserEmail)
                .find();

            if (userQuery.items.length === 0) {
                this.showError("No matching user found. Please make sure you are registered.");
                return;
            }

            const userType = userQuery.items[0].userType;

            if (userType !== "student") {
                $w("#errorMessage").text = "Access denied. Only students can view feedback.";
                $w("#errorMessage").show();
                return;
            }

            await this.populateRoundDropdown();

            // Set event handlers
            $w("#dropdown2").onChange(() => this.onRoundChange());
            $w("#dropdown1").onChange(() => this.onCaseStudyChange());
        } catch (error) {
            console.error("Error initializing page:", error);
            this.showError("An error occurred. Please try again later.");
        }
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

            $w("#dropdown2").options = roundOptions;
        } catch (error) {
            console.error("Error querying roundInfo collection:", error);
            this.showError("Error loading round options. Please try again.");
        }
    }

    async onRoundChange() {
        const selectedRound = $w("#dropdown2").value;
        if (!selectedRound) {
            this.showError("Please select a valid round.");
            return;
        }

        await this.populateCaseStudyDropdown(selectedRound);
    }

    async populateCaseStudyDropdown(selectedRound) {
        try {
            const roundResults = await wixData.query("roundInfo")
                .eq("roundNum", selectedRound)
                .find();

            if (roundResults.items.length === 0) {
                this.showError("No matching round found.");
                return;
            }

            const roundId = roundResults.items[0]._id;
            const caseStudyResults = await wixData.query("CaseStudies")
                .eq("roundNum", roundId)
                .find();

            const caseStudyOptions = caseStudyResults.items.map(item => ({
                label: item.caseStudyName,
                value: item._id
            }));

            $w("#dropdown1").options = caseStudyOptions;
        } catch (error) {
            console.error("Error querying case studies:", error);
            this.showError("Error loading case studies. Please try again.");
        }
    }

    async onCaseStudyChange() {
        const selectedCaseStudy = $w("#dropdown1").value;
        if (!selectedCaseStudy) {
            this.showError("Please select a valid case study.");
            return;
        }

        await this.displayFeedback(selectedCaseStudy);
    }

    async displayFeedback(caseStudyID) {
        try {
            const userQuery = await wixData.query("userInfo")
                .eq("emailAddress", this.currentUserEmail)
                .find();

            if (userQuery.items.length === 0) {
                this.showError("No matching user found. Please make sure you are registered.");
                return;
            }

            const userId = userQuery.items[0]._id;

            const submissionQuery = await wixData.query("submissions")
                .eq("studentID", userId)
                .eq("caseStudyID", caseStudyID)
                .find();

            if (submissionQuery.items.length === 0) {
                this.showError("You haven't made a submission for the selected case study.");
                this.hideAllBoxes();
                return;
            }

            const submissionID = submissionQuery.items[0]._id;

            const feedbackQuery = await wixData.query("feedbackTable")
                .eq("submissionID", submissionID)
                .eq("gradedStatus", true) // Only fetch feedback with gradedStatus = true
                .find();

            if (feedbackQuery.items.length === 0) {
                this.showError("No graded feedback has been released for this case study yet.");
                this.hideAllBoxes();
                return;
            }

            const feedback = Feedback.fromWixData(feedbackQuery.items[0]); // Create Feedback instance

            this.updateUIWithFeedback(feedback);
        } catch (error) {
            console.error("Error displaying feedback:", error);
            this.showError("An error occurred while retrieving feedback. Please try again.");
        }
    }

    updateUIWithFeedback(feedback) {
        $w("#feedbackT").text = feedback.feedbackT;
        $w("#scoreT").text = feedback.scoreT;

        $w("#feedbackDd").text = feedback.feedbackDd;
        $w("#scoreDd").text = feedback.scoreDd;

        $w("#feedbackSd").text = feedback.feedbackSd;
        $w("#scoreSd").text = feedback.scoreSd;

        $w("#feedbackCt").text = feedback.feedbackCt;
        $w("#scoreCt").text = feedback.scoreCt;

        $w("#totalScore").text = feedback.totalScore;

        [
            "#box1", "#box2", "#box3", "#box4", "#box28",
            "#text79", "#text76", "#text91", "#text89",
            "#text87", "#text85", "#text83", "#text81", "#text92",
            "#feedbackT", "#feedbackDd", "#feedbackSd", "#feedbackCt",
            "#scoreT", "#scoreDd", "#scoreSd", "#scoreCt", "#totalScore"
        ].forEach(id => $w(id).show());
    }

    hideAllBoxes() {
        ["#box1", "#box2", "#box3", "#box4", "#box28"].forEach(id => $w(id).hide());
    }

    showError(message) {
        $w("#errorMessage").text = message;
        $w("#errorMessage").show(); 
    }

    hideError() {
        $w("#errorMessage").hide();
    }
}

// Initialize the class
$w.onReady(() => {
    const feedbackManager = new FeedbackDisplayManager();
    feedbackManager.init();
});
