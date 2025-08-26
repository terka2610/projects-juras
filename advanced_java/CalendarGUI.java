package model;

import javax.swing.*;
import java.awt.*;
import java.time.*;
import java.util.Date;
import java.util.Calendar;
import java.text.SimpleDateFormat;

public class CalendarGUI extends JDialog {
    private final JSpinner dateSpinner;   
    private final JSpinner timeSpinner;   
    private LocalDateTime result = null;

    private CalendarGUI(Window parent, LocalDateTime initial) {
        super(parent, "Select Date & Time", ModalityType.APPLICATION_MODAL);

        // initial date/time
        LocalDateTime init = (initial != null) ? initial : LocalDateTime.now().plusDays(1).withSecond(0).withNano(0);

        // Convert LocalDateTime to java.util.Date
        java.util.Calendar cal = java.util.Calendar.getInstance();
        cal.set(init.getYear(), init.getMonthValue() - 1, init.getDayOfMonth(), 0, 0, 0);
        Date initDate = cal.getTime();

        // Date 
        SpinnerDateModel dateModel = new SpinnerDateModel(initDate, null, null, java.util.Calendar.DAY_OF_MONTH);
        dateSpinner = new JSpinner(dateModel);
        dateSpinner.setEditor(new JSpinner.DateEditor(dateSpinner, "yyyy-MM-dd"));

        // Time 
        cal.set(java.util.Calendar.HOUR_OF_DAY, init.getHour());
        cal.set(java.util.Calendar.MINUTE, init.getMinute());
        Date initTime = cal.getTime();

        SpinnerDateModel timeModel = new SpinnerDateModel(initTime, null, null, java.util.Calendar.MINUTE);
        timeSpinner = new JSpinner(timeModel);
        timeSpinner.setEditor(new JSpinner.DateEditor(timeSpinner, "HH:mm"));

        // Button
        JButton ok = new JButton("OK");
        JButton cancel = new JButton("Cancel");

        ok.addActionListener(e -> {
            // merge into LocalDateTime
            Date d = (Date) dateSpinner.getValue();
            Date t = (Date) timeSpinner.getValue();

            java.util.Calendar cd = java.util.Calendar.getInstance();
            cd.setTime(d);
            java.util.Calendar ct = java.util.Calendar.getInstance();
            ct.setTime(t);

            int year = cd.get(java.util.Calendar.YEAR);
            int month = cd.get(java.util.Calendar.MONTH) + 1;
            int day = cd.get(java.util.Calendar.DAY_OF_MONTH);
            int hour = ct.get(java.util.Calendar.HOUR_OF_DAY);
            int minute = ct.get(java.util.Calendar.MINUTE);

            result = LocalDateTime.of(year, month, day, hour, minute);
            dispose();
        });
        cancel.addActionListener(e -> { result = null; dispose(); });

        // Layout
        JPanel form = new JPanel(new GridLayout(2, 2, 8, 8));
        form.add(new JLabel("Date (yyyy-MM-dd):"));
        form.add(dateSpinner);
        form.add(new JLabel("Time (HH:mm):"));
        form.add(timeSpinner);

        JPanel btns = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        btns.add(ok);
        btns.add(cancel);

        getContentPane().setLayout(new BorderLayout(10, 10));
        getContentPane().add(form, BorderLayout.CENTER);
        getContentPane().add(btns, BorderLayout.SOUTH);
        getRootPane().setDefaultButton(ok);

        pack();
        setLocationRelativeTo(parent);
    }

    // shows the date/time picker dialog and returns the selected value.
    public static LocalDateTime showDialog(Window parent, LocalDateTime initial) {
        CalendarGUI dlg = new CalendarGUI(parent, initial);
        dlg.setVisible(true);
        return dlg.result;
    }
}
