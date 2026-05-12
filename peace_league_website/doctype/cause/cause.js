frappe.ui.form.on("Cause", {
    refresh(frm) {
        if (frm.doc.goal_amount && frm.doc.raised_amount) {
            let percent = Math.min((frm.doc.raised_amount / frm.doc.goal_amount) * 100, 100);
            frm.dashboard.add_progress("Fundraising Progress", percent, "Raised " + frm.doc.raised_amount + " of " + frm.doc.goal_amount);
        }
    }
});
