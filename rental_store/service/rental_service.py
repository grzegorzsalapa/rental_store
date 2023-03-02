from datetime import date, timedelta

from rental_store.models import Film, FilmReturnRequest, ReturnFilmResponse, FilmRentRequestModel
from rental_store.repository.data_storage import FilmRentalDetails, Rental, InMemoryRentalsRepository, \
    InMemoryFilmRepository
from rental_store.service.price_calculator import PriceCalculator


class RentalService:

    # Instead of creating/hard-coding repositories in this module, I'll pass them as arguments - then I'll be able to
    # INJECT the dependencies of the Rentals Service (see I in SOLID)
    def __init__(self,
                 film_repository: InMemoryFilmRepository,
                 rental_repository: InMemoryRentalsRepository,
                 calculator: PriceCalculator):
        self.film_repository = film_repository
        self.rental_repository = rental_repository
        self.calculator = calculator

    # assumptions:
    # 1. we allow partial rentals in case some movies are not available
    # 2. we allow only 1 rental per customer
    def rent_films(self, request: FilmRentRequestModel) -> list[FilmRentalDetails]:
        not_available_films: set[Film] = set()
        film_rental_details: set[FilmRentalDetails] = set()

        for film_to_be_rented in request.rented_films:  # TODO rename to films_to_rent in the request
            detail = self.film_repository.films.get(film_to_be_rented.film_id)
            if detail.available_items > 0:  # TODO: refactor - magic number
                # TODO: currency not used
                charge, currency = self.calculator.calculate_rent_charge(detail, film_to_be_rented.up_front_days)
                film_rental_detail = FilmRentalDetails(film_id=film_to_be_rented.film_id,
                                                       rental_date=date.today(),
                                                       charged=charge,
                                                       up_front_days=film_to_be_rented.up_front_days)
                film_rental_details.add(film_rental_detail)
            else:
                not_available_films.add(film_to_be_rented.film_id)

        for detail in film_rental_details:
            self.film_repository.mark_as_rented(detail.film_id)

        self.rental_repository.save(Rental(customer_id=request.customer_id, details=film_rental_details))

        return film_rental_details

    # assumptions:
    # 1. customer must pay upon the return
    # 2. customer might return only a subset of already rented movies
    # 3. for the movies not returned now, customer will not pay surcharge, it will be calculated when returned
    # 4. if customer returns a movie earlier than up_font_days, no money will be returned to the customer
    def return_films(self, request: FilmReturnRequest) -> ReturnFilmResponse:
        rental = self.rental_repository.find_by_customer_id(request.customer_id)

        for returned_film in request.returned_films:
            rented_film_details = rental.details.pop(returned_film)

            total_surcharge = 0
            if date.today() > rented_film_details.rental_date + timedelta(days=rented_film_details.up_front_days3):
                film = self.film_repository.find_film(rented_film_details.film_id)
                surcharge = self.calculator.calculate_rent_surcharge(film, rented_film_details.up_front_days)
                total_surcharge += surcharge

            self.film_repository.mark_as_returned(returned_film)
            self.rental_repository.save(rental)

        return ReturnFilmResponse(total_surcharge)
