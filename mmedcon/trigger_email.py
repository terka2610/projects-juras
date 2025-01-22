import { triggeredEmails } from 'wix-crm-backend';

export async function sendComplaintEmail(emailKey, memberId, variables) {
    try {
        const response = await triggeredEmails.emailMember(emailKey, memberId, { variables });
        console.log("Triggered email sent successfully:", response);
        return response;
    } catch (error) {
        console.error("Error sending triggered email:", error);
        throw error;
    }
}

export async function sendResolvedEmail(emailKey, memberId, variables) {
    try {
        // Send the triggered email
        const response = await triggeredEmails.emailMember(emailKey, memberId, {
            variables: {
                complaintID: variables.complaintID, // Pass only the necessary variable
            },
        });


        console.log("Resolved email sent successfully:", response);
        return response; // Return response for logging or debugging if needed
    } catch (error) {
        console.error("Error sending resolved email:", error);
        throw error; // Ensure the error bubbles up to the frontend
    }
}
