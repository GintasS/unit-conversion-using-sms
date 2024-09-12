// Identifiers for manipulation.
const UNIT_CATEGORY = "#categories-menu",
    UNIT_FROM = "#sub-units-menu-from",
    UNIT_TO = "#sub-units-menu-to",
    UNIT_VALUE = "#fromUnitValue",
    CONVERT_BTN = "#buttonConvert",
    RESULT = "#result";
    SMS_CONVERSION_EXAMPLE = "#sms-conversion-example"

// Holds current category.
// This is used for reset purposes.
var currentCategory = "";

// Disable drop-down lists after website has loaded.
function InitOnStart()
{
    $(UNIT_FROM).prop('disabled', true);
    $(UNIT_TO).prop('disabled', true);
    $(CONVERT_BTN).prop('disabled', true);
    $(UNIT_VALUE).prop('disabled', true);
}

// Initialize event to display sub units for a specific category.
function InitSubUnitDisplay()
{
    $(UNIT_CATEGORY).change(function (e)
    {
        // Clear previous sub-units.
        $(UNIT_FROM).empty();
        $(UNIT_TO).prop('disabled', true);
        $(UNIT_FROM).prop('disabled', true);
        $(UNIT_VALUE).prop('disabled', true);

        // When user changes the category, reset drop-downs.
        if (currentCategory != $(UNIT_CATEGORY).val() &&
            currentCategory.length != 0)
        {
            $(UNIT_TO).empty();
            $(UNIT_TO).prop('disabled', true);
            $(UNIT_VALUE).val('');
        }

        // Enable unit from drop-down & value field.
        $(UNIT_FROM).prop('disabled', false);

        $(UNIT_FROM).change(function() {
            $(UNIT_TO).prop('disabled', false);
        });

        $(UNIT_TO).change(function() {
            $(UNIT_VALUE).prop('disabled', false);
        });

        // Get sub-units.
        $.ajax({
            url: '/units-update?userCategory=' + $(UNIT_CATEGORY).val(),
            success: function (data)
            {
                // Remove the first one or "Unit FROM".
                $(UNIT_FROM).slice(1).remove();
                


                // Fill the units.
                FillSubUnits(data["subUnits"])
            }
        });

        currentCategory = $(UNIT_CATEGORY).val();
        e.preventDefault();
    });
}

// Initialize event on "Convert" button click.
function InitConversionMechanism()
{
    $(CONVERT_BTN).click(function (e)
    {
        $.ajax({
            url: "/convert?userCategory=" + $(UNIT_CATEGORY).val() +
                "&unitFrom=" + $(UNIT_FROM).val() +
                "&unitFromAmount=" + $(UNIT_VALUE).val() +
                "&unitTo=" + $(UNIT_TO).val(),
            success: function (data)
            {
                $(RESULT).text(data["result"]);
                $(SMS_CONVERSION_EXAMPLE).text("CONVERT " + $(UNIT_CATEGORY).val() + "/" + $(UNIT_FROM).val() + "/" + $(UNIT_TO).val() + "/" + $(UNIT_VALUE).val())
            }
        });
        e.preventDefault();
    });
}

// Initialize other events.
function InitEvents()
{
    // Sequence:
    // Select a category -> 
    // select unit from -> 
    // select unit to -> 
    // select unit value -> 
    // convert button becomes active.

    $(UNIT_VALUE).on("input", function (e)
    {
        // Get input field value.
        var number = parseFloat($(UNIT_VALUE).val())

        // Validate user input.
        if (isNaN(number) || number < 0)
        {
            $(UNIT_VALUE).val('');
            $(UNIT_TO).prop('disabled', true);
        }
        else
        {
            $(UNIT_TO).prop('disabled', false);
        }
        e.preventDefault();
    });

    // Activate "Convert" button when unit to was selected.
    $(UNIT_TO).change(function (e)
    {
        $(CONVERT_BTN).prop('disabled', false);
        e.preventDefault();
    });
}

// Helper function to fill sub units to a specific drop-down.
function FillSubUnits(data)
{
    let len = data.length
    for (i = 0; i < len; i++)
    {
        $(UNIT_FROM).append("<option data-toggle='tooltip' data-placement='top' title='" + data[i]["desc"] +"'>" + data[i]["unit"] + "</option>");
        $(UNIT_TO).append("<option data-toggle='tooltip' data-placement='top' title='" + data[i]["desc"] + "'>" + data[i]["unit"] + "</option>");
    }
}