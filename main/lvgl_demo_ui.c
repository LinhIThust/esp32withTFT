/*
 * SPDX-FileCopyrightText: 2021-2022 Espressif Systems (Shanghai) CO LTD
 *
 * SPDX-License-Identifier: CC0-1.0
 */

// This demo UI is adapted from LVGL official example: https://docs.lvgl.io/master/widgets/extra/meter.html#simple-meter

#include "lvgl.h"

static lv_obj_t *meter;
static lv_obj_t *calendar;
static lv_obj_t * btn;
static lv_disp_rot_t rotation = LV_DISP_ROT_NONE;

static void set_value(void *indic, int32_t v)
{
    lv_meter_set_indicator_end_value(meter, indic, v);
}

static void btn_cb(lv_event_t * e)
{
    lv_disp_t *disp = lv_event_get_user_data(e);
    rotation++;
    if (rotation > LV_DISP_ROT_270) {
        rotation = LV_DISP_ROT_NONE;
    }
    lv_disp_set_rotation(disp, rotation);
}

void example_lvgl_demo_ui(lv_disp_t *disp)
{
    lv_obj_t *scr = lv_disp_get_scr_act(disp);
    meter = lv_meter_create(scr);
    lv_obj_center(meter);
    lv_obj_set_size(meter, 200, 200);

    /*Add a scale first*/
    lv_meter_scale_t *scale = lv_meter_add_scale(meter);
    lv_meter_set_scale_ticks(meter, scale, 41, 2, 10, lv_palette_main(LV_PALETTE_GREY));
    lv_meter_set_scale_major_ticks(meter, scale, 8, 4, 15, lv_color_black(), 10);

    lv_meter_indicator_t *indic;

    /*Add a blue arc to the start*/
    indic = lv_meter_add_arc(meter, scale, 3, lv_palette_main(LV_PALETTE_BLUE), 0);
    lv_meter_set_indicator_start_value(meter, indic, 0);
    lv_meter_set_indicator_end_value(meter, indic, 20);

    /*Make the tick lines blue at the start of the scale*/
    indic = lv_meter_add_scale_lines(meter, scale, lv_palette_main(LV_PALETTE_BLUE), lv_palette_main(LV_PALETTE_BLUE), false, 0);
    lv_meter_set_indicator_start_value(meter, indic, 0);
    lv_meter_set_indicator_end_value(meter, indic, 20);

    /*Add a red arc to the end*/
    indic = lv_meter_add_arc(meter, scale, 3, lv_palette_main(LV_PALETTE_RED), 0);
    lv_meter_set_indicator_start_value(meter, indic, 80);
    lv_meter_set_indicator_end_value(meter, indic, 100);

    /*Make the tick lines red at the end of the scale*/
    indic = lv_meter_add_scale_lines(meter, scale, lv_palette_main(LV_PALETTE_RED), lv_palette_main(LV_PALETTE_RED), false, 0);
    lv_meter_set_indicator_start_value(meter, indic, 80);
    lv_meter_set_indicator_end_value(meter, indic, 100);

    /*Add a needle line indicator*/
    indic = lv_meter_add_needle_line(meter, scale, 4, lv_palette_main(LV_PALETTE_GREEN), -10);
}

//chang UI here
void example_lvgl_demo_ui2(lv_disp_t *disp) {
    lv_color16_t c;
    c.full = 0x5345;
    disp->bg_color = c;
    lv_obj_t *scr = lv_disp_get_scr_act(disp);
    calendar = lv_calendar_create(scr);
    // lv_obj_remove_style_all(calendar);
    lv_obj_center(calendar);
    lv_obj_set_size(calendar, 170, 170);

    //setdata
    lv_calendar_set_today_date(calendar,2024,9,17);
    lv_calendar_set_showed_date(calendar,2024,9);

    static lv_style_t style;
    lv_style_init(&style);
    // lv_style_set_radius(&style, LV_RADIUS_CIRCLE);
    lv_style_value_t v;
    v.color.full = 0x5345;
    lv_style_set_prop(&style,LV_STYLE_BORDER_COLOR,v);
    // LV_STYLE_BORDER_COLOR
    lv_obj_add_style(calendar, &style, 0);
}
    