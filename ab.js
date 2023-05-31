function CalendarControl() {
    const r = new Date(),
        o = {
            localDate: new Date(),
            prevMonthLastDate: null,
            calWeekDays: ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"],
            calMonthName: [
                "Jan",
                "Feb",
                "Mar",
                "Apr",
                "May",
                "Jun",
                "Jul",
                "Aug",
                "Sep",
                "Oct",
                "Nov",
                "Dec",
            ],
            daysInMonth: function (e, t) {
                return new Date(t, e, 0).getDate();
            },
            firstDay: function () {
                return new Date(r.getFullYear(), r.getMonth(), 1);
            },
            lastDay: function () {
                return new Date(r.getFullYear(), r.getMonth() + 1, 0);
            },
            firstDayNumber: function () {
                return o.firstDay().getDay() + 1;
            },
            lastDayNumber: function () {
                return o.lastDay().getDay() + 1;
            },
            getPreviousMonthLastDate: function () {
                return new Date(r.getFullYear(), r.getMonth(), 0).getDate();
            },
            navigateToPreviousMonth: function () {
                r.setMonth(r.getMonth() - 1);
                o.attachEventsOnNextPrev();
            },
            navigateToNextMonth: function () {
                r.setMonth(r.getMonth() + 1);
                o.attachEventsOnNextPrev();
            },
            navigateToCurrentMonth: function () {
                var e = o.localDate.getMonth(),
                    t = o.localDate.getFullYear();
                r.setMonth(e);
                r.setYear(t);
                o.attachEventsOnNextPrev();
            },
            displayYear: function () {
                let e = document.querySelector(
                    ".calendar .calendar-year-label"
                );
                e.innerHTML = r.getFullYear();
            },
            displayMonth: function () {
                let e = document.querySelector(
                    ".calendar .calendar-month-label"
                );
                e.innerHTML = o.calMonthName[r.getMonth()];
            },
            selectDate: function(e) {
                const selectedDate = new Date(r.getFullYear(), r.getMonth(), e.target.textContent);
                const currentDate = new Date();
                if (selectedDate >= currentDate) {
                  const dateStr = e.target.textContent + "/" + (r.getMonth() + 1) + "/" + r.getFullYear();
                  setHQTCalendar(dateStr, r.getFullYear() + "-" + (r.getMonth() + 1) + "-" + e.target.textContent);
                } else {
                  // Handle error or show a message that the date is in the past
                  console.log("Selected date is in the past");
                  alert('Please select a date in the future');
                }
            },
              
            plotSelectors: function () {
                document.querySelector(
                    ".calendar"
                ).innerHTML += `<div class="calendar-inner"><div class="calendar-controls"><div class="calendar-prev"><a href="#"><svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128"><path fill="#666" d="M88.2 3.8L35.8 56.23 28 64l7.8 7.78 52.4 52.4 9.78-7.76L45.58 64l52.4-52.4z"/></svg></a></div><div class="calendar-year-month"><div class="calendar-month-label"></div><div>-</div><div class="calendar-year-label"></div></div><div class="calendar-next"><a href="#"><svg xmlns="http://www.w3.org/2000/svg" width="128" height="128" viewBox="0 0 128 128"><path fill="#666" d="M38.8 124.2l52.4-52.42L99 64l-7.77-7.78-52.4-52.4-9.8 7.77L81.44 64 29 116.42z"/></svg></a></div></div><div class="calendar-today-date">Today: ${
                    o.calWeekDays[o.localDate.getDay()]
                }, ${o.localDate.getDate()}, ${
                    o.calMonthName[o.localDate.getMonth()]
                } ${o.localDate.getFullYear()}</div><div class="calendar-body"></div></div>`;
            },
            plotDayNames: function () {
                for (let e = 0; e < o.calWeekDays.length; e++)
                    document.querySelector(
                        ".calendar .calendar-body"
                    ).innerHTML += `<div>${o.calWeekDays[e]}</div>`;
            },
            plotDates: function () {
                document.querySelector(".calendar .calendar-body").innerHTML =
                    "";
                o.plotDayNames();
                o.displayMonth();
                o.displayYear();
                let t = 1,
                    a = 0,
                    n =
                        ((o.prevMonthLastDate = o.getPreviousMonthLastDate()),
                        []);
                var l = o.daysInMonth(r.getMonth() + 1, r.getFullYear());
                for (let e = 1; e < l; e++)
                    if (e < o.firstDayNumber()) {
                        a += 1;
                        document.querySelector(
                            ".calendar .calendar-body"
                        ).innerHTML += '<div class="prev-dates"></div>';
                        n.push(o.prevMonthLastDate--);
                    } else
                        document.querySelector(
                            ".calendar .calendar-body"
                        ).innerHTML += `<div class="number-item" data-num=${t}><a class="dateNumber" href="#">${t++}</a></div>`;
                for (let e = 0; e < a + 1; e++)
                    document.querySelector(
                        ".calendar .calendar-body"
                    ).innerHTML += `<div class="number-item" data-num=${t}><a class="dateNumber" href="#">${t++}</a></div>`;
                o.highlightToday();
                o.plotPrevMonthDates(n);
                o.plotNextMonthDates();
            },
            attachEvents: function () {
                let e = document.querySelector(".calendar .calendar-prev a"),
                    t = document.querySelector(".calendar .calendar-next a"),
                    a = document.querySelector(
                        ".calendar .calendar-today-date"
                    ),
                    n = document.querySelectorAll(".calendar .dateNumber");
                e.addEventListener("click", o.navigateToPreviousMonth);
                t.addEventListener("click", o.navigateToNextMonth);
                a.addEventListener("click", o.navigateToCurrentMonth);
                for (var l = 0; l < n.length; l++)
                    n[l].addEventListener("click", o.selectDate, !1);
            },
            highlightToday: function () {
                var e = o.localDate.getMonth() + 1,
                    t = r.getMonth() + 1;
                o.localDate.getFullYear() === r.getFullYear() &&
                    e === t &&
                    document.querySelectorAll(".number-item") &&
                    document
                        .querySelectorAll(".number-item")
                        [r.getDate() - 1].classList.add("calendar-today");
            },
            plotPrevMonthDates: function (t) {
                t.reverse();
                for (let e = 0; e < t.length; e++)
                    document.querySelectorAll(".prev-dates") &&
                        (document.querySelectorAll(".prev-dates")[
                            e
                        ].textContent = t[e]);
            },
            plotNextMonthDates: function () {
                var e = document.querySelector(".calendar-body")
                    .childElementCount;
                if (42 < e) {
                    var t = 49 - e;
                    o.loopThroughNextDays(t);
                }
                if (35 < e && e <= 42) o.loopThroughNextDays(42 - e);
            },
            loopThroughNextDays: function (t) {
                if (0 < t)
                    for (let e = 1; e <= t; e++)
                        document.querySelector(
                            ".calendar-body"
                        ).innerHTML += `<div class="next-dates">${e}</div>`;
            },
            attachEventsOnNextPrev: function () {
                o.plotDates();
                o.attachEvents();
            },
            init: function () {
                o.plotSelectors();
                o.plotDates();
                o.attachEvents();
            },
        };
    o.init();
}
