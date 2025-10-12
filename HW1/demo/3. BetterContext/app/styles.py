"""Centralized CSS class styles to reduce duplication across UI components."""

# Button styles
BUTTON_STYLES = {
    "template": "btn btn-outline w-full text-left h-auto py-4 mb-3",
    "primary": "btn btn-primary",
    "info": "btn btn-info",
    "error": "btn btn-error",
    "ghost": "btn btn-ghost",
    "success": "btn btn-success",
    "primary_xs": "btn btn-xs btn-primary",
    "error_xs": "btn btn-xs btn-error",
    "ghost_xs": "btn btn-xs btn-ghost",
    "success_xs": "btn btn-xs btn-success",
}

# Heading styles
HEADING_STYLES = {
    "h2": "text-2xl font-bold mb-4",
    "h3": "text-lg font-semibold mb-2",
    "h4": "font-bold text-lg mb-1",
}

# Container/Layout styles
CONTAINER_STYLES = {
    "column": "border border-base-300 p-4",
    "card": "card bg-base-100 shadow-lg p-4 mb-3",
    "modal_box": "modal-box",
    "grid_3col": "grid grid-cols-3 gap-4 w-full",
}

# Text styles
TEXT_STYLES = {
    "small": "text-sm",
    "extra_small": "text-xs",
    "bold": "font-bold",
    "semibold": "font-semibold",
}

# Form styles
FORM_STYLES = {
    "control": "form-control",
    "label": "label",
    "select": "select select-bordered w-full",
    "select_sm": "select select-bordered select-sm w-full",
    "textarea": "textarea textarea-bordered w-full",
    "textarea_sm": "textarea textarea-bordered textarea-sm w-full",
    "input": "input input-bordered w-full",
    "input_sm": "input input-bordered input-sm w-full",
}

# Spacing styles
SPACING_STYLES = {
    "mb_2": "mb-2",
    "mb_3": "mb-3",
    "mb_4": "mb-4",
    "mt_2": "mt-2",
    "mt_6": "mt-6",
    "mr_1": "mr-1",
    "mr_2": "mr-2",
}

# Act/Section styles for timeline
ACT_STYLES = {
    "act1": "bg-green-50 p-3 rounded mb-3",
    "act2": "bg-blue-50 p-3 rounded mb-3",
    "act3": "bg-purple-50 p-3 rounded",
    "act1_header": "font-bold text-green-700 mb-2",
    "act2_header": "font-bold text-blue-700 mb-2",
    "act3_header": "font-bold text-purple-700 mb-2",
}

# List styles
LIST_STYLES = {
    "disc_inside": "list-disc list-inside space-y-1",
}

# Utility styles
UTILITY_STYLES = {
    "flex_gap_2": "flex gap-2",
    "flex_col_gap_3": "flex flex-col gap-3",
    "italic_gray": "text-gray-500 italic text-sm",
}
