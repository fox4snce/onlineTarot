let major_arcana = ["The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor", "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit", "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance", "The Devil", "The Tower", "The Star", "The Moon", "The Sun", "Judgement", "The World"];
    let minor_arcana = [];
    let suits = ["Wands", "Cups", "Swords", "Pentacles"];
    let ranks = ["Ace"].concat(Array.from({length: 10}, (_, i) => i + 2), ["Page", "Knight", "Queen", "King"]);
    suits.forEach(suit => {
        ranks.forEach(rank => {
            minor_arcana.push(`${rank} of ${suit}`);
        });
    });
    let tarot_cards = major_arcana.concat(minor_arcana);

    // Create card selection dropdowns for Celtic Cross spread (10 cards)
    var cardSelects = [];
    for (var i = 1; i <= 10; i++) {
        var select = $("<select></select>").attr("id", "card_" + i).attr("name", "card_" + i);
        tarot_cards.forEach(function(card) {
            select.append($("<option></option>").attr("value", card).text(card));
        });

        select.change(function() {
            refreshDisabledStatus();
        });

        cardSelects.push(select);

        var checkbox = $("<input type='checkbox' id='reversed_" + i + "' name='reversed_" + i + "' value='reversed'>Reversed<br>");
        if (i <= 5) {
            $("#left_cards").append($("<label></label>").attr("for", "card_" + i).text("Card " + i + ": "));
            $("#left_cards").append(select);
            $("#left_cards").append(checkbox);
            $("#left_cards").append("<br>");
        } else {
            $("#right_cards").append($("<label></label>").attr("for", "card_" + i).text("Card " + i + ": "));
            $("#right_cards").append(select);
            $("#right_cards").append(checkbox);
            $("#right_cards").append("<br>");
        }
    }

    function refreshDisabledStatus() {
        // Enable all options in all dropdowns
        cardSelects.forEach(function(selectElement) {
            selectElement.find('option').prop('disabled', false);
        });

        // Disable the selected card in all other dropdowns
        cardSelects.forEach(function(selectElement) {
            var selectedCard = selectElement.val();
            cardSelects.forEach(function(otherSelectElement) {
                if (otherSelectElement[0] !== selectElement[0]) {
                    otherSelectElement.find("option[value='" + selectedCard + "']").prop("disabled", true);
                }
            });
        });
    }

    // Function to draw a random card and its orientation
    function drawRandomCard() {
        let cardIndex = Math.floor(Math.random() * tarot_cards.length);
        let card = tarot_cards[cardIndex];
        let orientation = Math.random() < 0.5 ? 'reversed' : 'upright';

        // Remove the card from the deck
        tarot_cards.splice(cardIndex, 1);

        return [card, orientation];
    }

    // Handle form submission
    $("#tarotForm").submit(function(e) {
        e.preventDefault();

        var hand = [];
        for (var i = 1; i <= 10; i++) {
            var card = $("#card_" + i).val();
            var orientation = $("#reversed_" + i).is(":checked") ? 'reversed' : 'upright';
            hand.push([card, orientation]);
        }

        var data = {
            name: $("#name").val(),
            question: $("#question").val(),
            spread_choice: $("#spread_choice").val(),
            hand: hand
        };

        $.ajax({
            type: "POST",
            url: "http://localhost:5000/api/reading",
            data: JSON.stringify(data),
            contentType: "application/json",
            dataType: "json",
            success: function(response) {
                localStorage.setItem('result', JSON.stringify(response));
                window.location.href = 'result.html';
            },
            error: function(err) {
                console.log('Error:', err);
            }
        });
    });

    // Handle random draw button click
    $("#drawRandom").click(function() {
        // Refresh card deck
        tarot_cards = major_arcana.concat(minor_arcana);

        for (var i = 1; i <= 10; i++) {
            var drawnCard = drawRandomCard();

            // Select the drawn card in dropdown
            $("#card_" + i).val(drawnCard[0]).change();

            // Set the orientation checkbox
            if (drawnCard[1] === 'reversed') {
                $("#reversed_" + i).prop('checked', true);
            } else {
                $("#reversed_" + i).prop('checked', false);
            }
        }

        refreshDisabledStatus();
    });